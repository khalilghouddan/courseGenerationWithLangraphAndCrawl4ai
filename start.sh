#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

python - <<'PY'
import os
import time
import psycopg2

host = os.getenv("DEEP_AGENT_DB_HOST", "db")
port = os.getenv("DEEP_AGENT_DB_PORT", "5432")
user = os.getenv("DEEP_AGENT_DB_USER", "postgres")
password = os.getenv("DEEP_AGENT_DB_PASSWORD", "root")

for attempt in range(60):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database="postgres",
        )
        conn.close()
        print("PostgreSQL is ready.")
        break
    except Exception as exc:
        if attempt == 59:
            raise
        print(f"PostgreSQL not ready yet: {exc}")
        time.sleep(2)
PY

echo "Initializing database..."
python scriptes/init_db.py

echo "Starting API..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8011
