### Settings file 
# from .env to project 
# no os lib is used


#importing pydantic's BaseSettings and SettingsConfigDict 
#insted of importing os and call .env we use settings file
from pydantic_settings import BaseSettings, SettingsConfigDict

#class setting herite de BASEsETTINGS
class Settings(BaseSettings):

    # key and baseUrl
    openai_api_key: str
    openai_base_url: str

    # Default model
    openai_model: str = "qwen3:8b"

    # Additional models
    OPENAI_MODEL_FAST: str = "qwen3:8b"
    OPENAI_MODEL_BALANCED: str = "mistral-small3.2:latest"
    OPENAI_MODEL_REASONING: str = "qwen3:8b"

    # Web Research
    web_research_api_key: str
    web_research_base_url: str

    # PostgreSQL
    deep_agent_db_host: str = "127.0.0.1"
    deep_agent_db_port: int = 5433
    deep_agent_db_user: str = "postgres"
    deep_agent_db_password: str

    #reading .env , stting the encoding to utf8
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

#creating the object
settings = Settings()