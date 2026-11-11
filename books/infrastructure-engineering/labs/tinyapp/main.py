"""tinyapp: a very small web app for the labs in this book."""
import os
from pathlib import Path

from fastapi import FastAPI

VERSION = os.environ.get("APP_VERSION", "dev")
DATABASE_URL = os.environ.get("DATABASE_URL", "")
DATA_FILE = Path(os.environ.get("DATA_DIR", "/tmp")) / "visits.txt"

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}


@app.get("/visits")
def visits():
    return {"visits": count_visit()}


def count_visit() -> int:
    if DATABASE_URL:
        return count_visit_in_postgres()
    count = int(DATA_FILE.read_text()) if DATA_FILE.exists() else 0
    DATA_FILE.write_text(str(count + 1))
    return count + 1


def count_visit_in_postgres() -> int:
    import psycopg  # only needed when DATABASE_URL is set

    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS visits (id int PRIMARY KEY, n int)")
        row = conn.execute(
            "INSERT INTO visits VALUES (1, 1) "
            "ON CONFLICT (id) DO UPDATE SET n = visits.n + 1 RETURNING n"
        ).fetchone()
    return row[0]
