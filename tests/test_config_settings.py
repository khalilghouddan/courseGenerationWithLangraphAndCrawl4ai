from app.utils import config


def test_settings_expose_health_related_defaults():
    settings = config.Settings(_env_file=".env", _env_file_encoding="utf-8")

    assert settings.search_url.startswith("http")
    assert settings.scrape_url.startswith("http")
    assert settings.llm_model
    assert settings.llm_api_key or settings.openai_api_key
