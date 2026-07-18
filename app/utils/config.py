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
    QUEN_MODEL: str | None = None
    # Additional models
    MISTRAL_MODEL: str | None = None

    # Web Research
    WEB_RESEARCH_API_KEY: str | None = None
    WEB_RESEARCH_BASE_URL: str | None = None

    # PostgreSQL
    DEEP_AGENT_DB_HOST: str | None = None
    DEEP_AGENT_DB_PORT: int | None = None
    DEEP_AGENT_DB_USER: str | None = None
    DEEP_AGENT_DB_PASSWORD: str | None = None

    #application 

    APP_PORT: int | None = None

    #reading .env , stting the encoding to utf8
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

# creating the object
settings = Settings()
