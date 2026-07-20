### Postgres connection ###

# Resposabilty:
#- database connection postgrese

#psycopg2 is postgres adaptaot for python
import psycopg2
#calling the settongs wsf
from app.utils.config import settings

#the center fuction to get connection
def get_db_connection():
    return psycopg2.connect(
        host=settings.DEEP_AGENT_DB_HOST,
        port=settings.DEEP_AGENT_DB_PORT,
        user=settings.DEEP_AGENT_DB_USER,
        password=settings.DEEP_AGENT_DB_PASSWORD,
        database="deep_agent_db",
    )