### Web Search Tool — SearXNG

#Responsibilities:
#- Send search queries to the SearXNG instance.
#- Return a deduplicated list of URLs for the scraper.

from typing import List
import requests

from app.utils.config import settings
from app.utils.logger import log_info


#build endpoint from config
_BASE_URL = (settings.WEB_RESEARCH_BASE_URL or "").rstrip("/")
_SEARCH_URL = f"{_BASE_URL}/web-research/search/search"
_HEADERS = {"X-API-Key": settings.WEB_RESEARCH_API_KEY or ""}


def search_web(queries: List[str], language: str = "en") -> List[str]:
    """
    Search the web using SearXNG for each query.
    Returns a deduplicated list of URLs.

    Args:
        queries:  List of search query strings.
        language: Language hint passed to SearXNG (e.g. "es", "fr", "en").
    """
    if not _BASE_URL or not settings.WEB_RESEARCH_API_KEY:
        log_info("WEB_SEARCH", "#E53935", "WEB_RESEARCH_BASE_URL or WEB_RESEARCH_API_KEY not set — returning empty results")
        return []

    seen: set = set()
    urls: List[str] = []
    max_per_query = settings.SearXNG_max_url  # URLs to take per query (SearXNG_max_url in .env)

    for query in queries:
        params = {
            "q": query,
            "format": "json",
            "language": language,
        }
        try:
            response = requests.get(
                _SEARCH_URL,
                headers=_HEADERS,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            results = response.json().get("results", [])

            count = 0
            for item in results:
                if count >= max_per_query:
                    break
                url = item.get("url")
                if url and url not in seen:
                    seen.add(url)
                    urls.append(url)
                    count += 1

        except Exception as e:
            log_info("WEB_SEARCH", "#E53935", f"Search failed for '{query}': {e}")

    return urls
