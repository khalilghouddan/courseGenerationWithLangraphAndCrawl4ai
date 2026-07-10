


#
import psycopg2 # type: ignore
from app.utils.config import settings
def get_db_connection():
    return psycopg2.connect(
        host=settings.deep_agent_db_host,
        port=settings.deep_agent_db_port,
        user=settings.deep_agent_db_user,
        password=settings.deep_agent_db_password,
        database="deep_agent_db"
    )