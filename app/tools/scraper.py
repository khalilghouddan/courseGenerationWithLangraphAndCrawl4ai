### Web Scraper Tool — Crawl4AI

#Responsibilities:
#- Scrape a batch of URLs via the Crawl4AI scrape endpoint.
#- Return clean Markdown content per URL.

from typing import List
import requests

from app.utils.config import settings
from app.utils.logger import log_info


#build endpoint from config
_BASE_URL = (settings.WEB_RESEARCH_BASE_URL or "").rstrip("/")
_SCRAPE_URL = f"{_BASE_URL}/web-research/crawl/scrape"
_HEADERS = {"X-API-Key": settings.WEB_RESEARCH_API_KEY or ""}
_BATCH_SIZE = settings.SCRAPED_IN_ONE_TIME  # from .env: SCRAPED_IN_ONE_TIME=3

#max characters to keep per page (to avoid blowing the LLM context)
MAX_CHARS = 10_000


def scrape_urls(urls: List[str]) -> List[str]:
    """
    Scrape the given URLs using Crawl4AI and return Markdown content.
    URLs are sent in a single batch request.

    Returns:
        List of strings, one per successfully scraped URL, formatted as:
        "Source URL: <url>\\n\\nContent:\\n<markdown>"
    """
    if not urls:
        return []

    if not _BASE_URL or not settings.WEB_RESEARCH_API_KEY:
        log_info("SCRAPER", "#E53935", "WEB_RESEARCH_BASE_URL or WEB_RESEARCH_API_KEY not set — skipping scrape")
        return []

    payload = {
        "urls": urls,
        "bypass_cache": False,
        "extract_links": False,
        "extract_summary": False,
        "batch_timeout_seconds": 120,
        "page_timeout_ms": 30_000,
    }

    documents: List[str] = []

    #split urls into chunks of SCRAPED_IN_ONE_TIME and make one request per chunk
    chunks = [urls[i:i + _BATCH_SIZE] for i in range(0, len(urls), _BATCH_SIZE)]
    log_info("SCRAPER", "#00BCD4", f"Scraping {len(urls)} URLs in {len(chunks)} batch(es) of up to {_BATCH_SIZE}")

    for chunk_idx, chunk in enumerate(chunks, start=1):
        payload = {
            "urls": chunk,
            "bypass_cache": False,
            "extract_links": False,
            "extract_summary": False,
            "batch_timeout_seconds": 120,
            "page_timeout_ms": 30_000,
        }

        try:
            response = requests.post(
                _SCRAPE_URL,
                headers=_HEADERS,
                json=payload,
                timeout=180,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            log_info("SCRAPER", "#E53935", f"Batch {chunk_idx} scrape request failed: {e}")
            continue

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

            documents.append(f"Source URL: {url}\n\nContent:\n{markdown}")
            log_info("SCRAPER", "#00BCD4", f"Scraped {len(markdown)} chars from {url}")

    return documents
