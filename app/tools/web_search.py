"""
Web Search Tool
"""

from typing import List
import os
from tavily import TavilyClient

def search_web(queries: List[str]) -> List[str]:
    """
    Search the web for the given queries and return a list of URLs.
    """
    tavily_api_key = os.environ.get("TAVILY_API_KEY")
    if not tavily_api_key:
        print("Warning: TAVILY_API_KEY environment variable is not set. Returning empty search results.")
        return []

    tavily_client = TavilyClient(api_key=tavily_api_key)
    
    urls = []
    for query in queries:
        try:
            # You can adjust search_depth to "advanced" if needed
            response = tavily_client.search(query=query, search_depth="basic")
            for result in response.get("results", []):
                urls.append(result["url"])
        except Exception as e:
            print(f"Error searching for '{query}': {e}")
            
    # Remove duplicates while preserving order
    unique_urls = []
    for url in urls:
        if url not in unique_urls:
            unique_urls.append(url)
            
    return unique_urls
