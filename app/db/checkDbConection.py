



import psycopg2

from app.utils.config import settings


def get_db_connection():
    return psycopg2.connect(
        host=settings.DEEP_AGENT_DB_HOST,
        port=settings.DEEP_AGENT_DB_PORT,
        user=settings.DEEP_AGENT_DB_USER,
        password=settings.DEEP_AGENT_DB_PASSWORD,
        database="deep_agent_db",
    )