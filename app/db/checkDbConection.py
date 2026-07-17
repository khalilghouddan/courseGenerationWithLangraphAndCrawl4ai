
from typing import Any

from app.utils.config import settings

try:
    import psycopg2  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    psycopg2 = None


def get_db_connection() -> Any:
    if psycopg2 is None:
        raise RuntimeError("psycopg2 is not installed")
    return psycopg2.connect(
        host=settings.deep_agent_db_host,
        port=settings.deep_agent_db_port,
        user=settings.deep_agent_db_user,
        password=settings.deep_agent_db_password,
        database="deep_agent_db",
    )