### Web Search Tool — SearXNG

# Responsibilities:
# - Send search queries to the SearXNG instance.
# - Return a deduplicated list of URLs for the scraper.
# - Async-first: search_web_async runs all queries concurrently.

import asyncio
from typing import List

import httpx

from app.utils.config import settings
from app.utils.logger import log_info


# Build endpoint from config
_BASE_URL = (settings.WEB_RESEARCH_BASE_URL or "").rstrip("/")
_SEARCH_URL = f"{_BASE_URL}/web-research/search/search"
_HEADERS = {"X-API-Key": settings.WEB_RESEARCH_API_KEY or ""}

# Per-query timeout (seconds)
_QUERY_TIMEOUT = 15


async def _search_single(
    client: httpx.AsyncClient,
    query: str,
    language: str,
    max_per_query: int,
) -> List[str]:
    """Run a single SearXNG query and return up to max_per_query URLs."""
    params = {"q": query, "format": "json", "language": language}
    try:
        response = await client.get(
            _SEARCH_URL,
            headers=_HEADERS,
            params=params,
            timeout=_QUERY_TIMEOUT,
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        urls = [item["url"] for item in results if item.get("url")]
        return urls[:max_per_query]
    except Exception as e:
        log_info("WEB_SEARCH", "#E53935", f"Search failed for '{query}': {e}")
        return []


async def search_web_async(queries: List[str], language: str = "en") -> List[str]:
    """
    Async: search SearXNG for all queries concurrently.
    Returns a deduplicated list of URLs.
    """
    if not _BASE_URL or not settings.WEB_RESEARCH_API_KEY:
        log_info("WEB_SEARCH", "#E53935", "WEB_RESEARCH_BASE_URL or WEB_RESEARCH_API_KEY not set — returning empty results")
        return []

    max_per_query = settings.SearXNG_max_url

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[_search_single(client, q, language, max_per_query) for q in queries],
            return_exceptions=False,
        )

    # Deduplicate while preserving order
    seen: set = set()
    urls: List[str] = []
    for batch in results:
        for url in batch:
            if url not in seen:
                seen.add(url)
                urls.append(url)

    return urls


def search_web(queries: List[str], language: str = "en") -> List[str]:
    """
    Sync wrapper — for use outside an async context (CLI / tests).
    Inside FastAPI, prefer search_web_async.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(asyncio.run, search_web_async(queries, language))
            return future.result()
    else:
        return asyncio.run(search_web_async(queries, language))
