### Web Scraper Tool — Crawl4AI

# Responsibilities:
# - Scrape a batch of URLs via the Crawl4AI scrape endpoint.
# - Return clean Markdown content per URL.
# - Use async httpx so the FastAPI event loop is never blocked.

import asyncio
from typing import List

import httpx

from app.utils.config import settings
from app.utils.logger import log_info


# Build endpoint from config
_BASE_URL = (settings.WEB_RESEARCH_BASE_URL or "").rstrip("/")
_SCRAPE_URL = f"{_BASE_URL}/web-research/crawl/scrape"
_HEADERS = {"X-API-Key": settings.WEB_RESEARCH_API_KEY or ""}
_BATCH_SIZE = settings.SCRAPED_IN_ONE_TIME  # from .env: SCRAPED_IN_ONE_TIME=3

# Max characters to keep per page (to avoid blowing the LLM context)
MAX_CHARS = 10_000

# Per-HTTP-request timeout (seconds). Keeps one bad URL from hanging everything.
_REQUEST_TIMEOUT = 30


async def _scrape_chunk(
    client: httpx.AsyncClient,
    chunk: List[str],
    chunk_idx: int,
) -> List[str]:
    """Send one batch request and return parsed documents."""
    payload = {
        "urls": chunk,
        "bypass_cache": False,
        "extract_links": False,
        "extract_summary": False,
        "batch_timeout_seconds": 20,   # server-side per-URL timeout
        "page_timeout_ms": 15_000,
    }

    try:
        response = await client.post(
            _SCRAPE_URL,
            headers=_HEADERS,
            json=payload,
            timeout=_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        log_info("SCRAPER", "#E53935", f"Batch {chunk_idx} scrape request failed: {e}")
        return []

    docs: List[str] = []
    for item in data.get("results", []):
        url = item.get("url", "")
        status = item.get("status", "")
        error = item.get("error")

        if error or status not in ("success", "ok", 200, "200"):
            log_info("SCRAPER", "#E53935", f"Failed [{status}] {url} — {error}")
            continue

        markdown = item.get("markdown") or item.get("markdown_raw") or ""
        if not markdown:
            continue

        if len(markdown) > MAX_CHARS:
            markdown = markdown[:MAX_CHARS] + "\n\n... [Content Truncated]"

        docs.append(f"Source URL: {url}\n\nContent:\n{markdown}")
        log_info("SCRAPER", "#00BCD4", f"Scraped {len(markdown)} chars from {url}")

    return docs


async def scrape_urls_async(urls: List[str]) -> List[str]:
    """
    Async version: scrape URLs using Crawl4AI without blocking the event loop.
    Batches run concurrently via asyncio.gather.
    """
    if not urls:
        return []

    if not _BASE_URL or not settings.WEB_RESEARCH_API_KEY:
        log_info("SCRAPER", "#E53935", "WEB_RESEARCH_BASE_URL or WEB_RESEARCH_API_KEY not set — skipping scrape")
        return []

    chunks = [urls[i:i + _BATCH_SIZE] for i in range(0, len(urls), _BATCH_SIZE)]
    log_info("SCRAPER", "#00BCD4", f"Scraping {len(urls)} URLs in {len(chunks)} batch(es) of up to {_BATCH_SIZE}")

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[_scrape_chunk(client, chunk, idx + 1) for idx, chunk in enumerate(chunks)],
            return_exceptions=False,
        )

    # Flatten list of lists
    documents: List[str] = [doc for batch in results for doc in batch]
    return documents


def scrape_urls(urls: List[str]) -> List[str]:
    """
    Sync wrapper — runs the async scraper on the current event loop if one
    exists (inside FastAPI), or creates a new one (CLI / tests).
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # We are inside an async context (FastAPI) — schedule as a coroutine
        # and block with run_until_complete is not safe; callers should use
        # scrape_urls_async() directly when possible.
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(asyncio.run, scrape_urls_async(urls))
            return future.result()
    else:
        return asyncio.run(scrape_urls_async(urls))
