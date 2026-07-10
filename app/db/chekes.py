


#
import requests
from langchain_openai import ChatOpenAI
from app.utils.logger import log_message
from app.utils.config import settings
from app.db.checkDbConection import get_db_connection




def check_db() -> tuple[str, str | None]:
    with log_message("HEALTH", "#00C853", "PostgreSQL DB"):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            return "up", None
        except Exception as e:
            return "down", str(e)


def check_search() -> tuple[str, str | None]:
    with log_message("HEALTH", "#00C853", "Search API"):
        try:
            response = requests.get(
                settings.search_url,
                headers=settings.web_research_headers,
                params={"q": "ping", "format": "json"},
                timeout=15,
            )
            if response.status_code == 200:
                return "up", None
            else:
                return "down", f"HTTP {response.status_code}: {response.text[:100]}"
        except Exception as e:
            return "down", str(e)


def check_crawl() -> tuple[str, str | None]:
    with log_message("HEALTH", "#00C853", "Crawl API"):
        try:
            # Send a fast OPTIONS request to verify the crawl endpoint is reachable
            response = requests.options(
                settings.scrape_url,
                headers=settings.web_research_headers,
                timeout=10,
            )
            # As long as the server responds (even with 405/422 etc), the service is up
            if response.status_code < 500:
                return "up", None
            else:
                return "down", f"HTTP {response.status_code}: {response.text[:100]}"
        except Exception as e:
            return "down", str(e)


def check_llm() -> tuple[str, str | None]:
    with log_message("HEALTH", "#00C853", "LLM (OpenAI)"):
        try:
            llm = ChatOpenAI(
                model=settings.llm_model,
                api_key=settings.llm_api_key,
                base_url=settings.llm_base_url if settings.llm_base_url else None,
                temperature=0.7,
            )
            llm.invoke("ping")
            return "up", None
        except Exception as e:
            return "down", str(e)
