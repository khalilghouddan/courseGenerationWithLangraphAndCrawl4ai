"""
Web Scraper Tool
"""

from typing import List
from langchain_community.document_loaders import WebBaseLoader
import re

def clean_text(text: str) -> str:
    """Clean the scraped text to remove excessive whitespace and newlines."""
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def scrape_urls(urls: List[str]) -> List[str]:
    """
    Scrape the given URLs and return their text content.
    Returns a list of strings where each string is the content of a document.
    """
    documents = []
    for url in urls:
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            
            # Combine the content of all documents from this URL
            text_content = "\n".join([doc.page_content for doc in docs])
            
            # Clean the text to save tokens
            text_content = clean_text(text_content)
            
            # Limit the content length to avoid exceeding LLM context windows
            max_chars = 10000 
            if len(text_content) > max_chars:
                text_content = text_content[:max_chars] + "... [Content Truncated]"
                
            doc_str = f"Source URL: {url}\n\nContent:\n{text_content}"
            documents.append(doc_str)
        except Exception as e:
            print(f"Error scraping '{url}': {e}")
            
    return documents
