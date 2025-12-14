import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "ideaforge.db"


def update_idea_status(idea_id: int, status: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "UPDATE idea SET status = ? WHERE id = ?",
        (status, idea_id),
    )

    conn.commit()
    conn.close()


def get_idea_status(idea_id: int) -> str | None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT status FROM idea WHERE id = ?",
        (idea_id,),
    )
    row = cur.fetchone()
    conn.close()

    return row[0] if row else None
