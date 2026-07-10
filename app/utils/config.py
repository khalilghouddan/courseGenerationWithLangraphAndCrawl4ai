


#
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str | None = None
    openai_base_url: str | None = None

    # ── Web Research API (replaces local SearXNG + Crawl4AI) ─────────────────
    web_research_base_url: str = "http://102.54.244.89:8088"
    web_research_api_key: str = "ws_sk_7fQ2mN9xLp4Vt5Lz1Fc6Rb3Bd5Uw0JaE"

    deep_agent_db_host: str = "127.0.0.1"
    deep_agent_db_port: int = 5433
    deep_agent_db_user: str = "postgres"
    deep_agent_db_password: str = "root"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def llm_model(self) -> str:
        return self.openai_model

    @property
    def llm_api_key(self) -> str | None:
        return self.openai_api_key

    @property
    def llm_base_url(self) -> str | None:
        return self.openai_base_url

    @property
    def web_research_headers(self) -> dict:
        return {"X-API-Key": self.web_research_api_key}

    @property
    def search_url(self) -> str:
        return self.web_research_base_url.rstrip("/") + "/web-research/search/search"

    @property
    def scrape_url(self) -> str:
        return self.web_research_base_url.rstrip("/") + "/web-research/crawl/scrape"

settings = Settings()
