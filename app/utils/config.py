### Settings file 
# from .env to project 
# no os lib is used


#importing pydantic's BaseSettings and SettingsConfigDict 
#insted of importing os and call .env we use settings file
from pydantic_settings import BaseSettings, SettingsConfigDict

#class setting herite de BASEsETTINGS
class Settings(BaseSettings):

    # key and baseUrl
    MODEL_API_KEY: str | None = None
    MODEL_BASE_URL: str | None = None

    # model default 
    QUEN_MODEL: str = "qwen3:8b"
    # Additional models
    MISTRAL_MODEL: str = "mistral-small3.2:latest"

    # Web Research
    WEB_RESEARCH_API_KEY: str | None = None
    WEB_RESEARCH_BASE_URL: str | None = None

    # PostgreSQL
    DEEP_AGENT_DB_HOST: str = "127.0.0.1"
    DEEP_AGENT_DB_PORT: int = 5433
    DEEP_AGENT_DB_USER: str = "postgres"
    DEEP_AGENT_DB_PASSWORD: str | None = None


    #reading .env , stting the encoding to utf8
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

# creating the object
settings = Settings()
