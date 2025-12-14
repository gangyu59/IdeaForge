import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "ideaforge.db"


def create_version(parent_idea_id: int, child_idea_id: int, source_round: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO idea_version (parent_idea_id, child_idea_id, source_round)
        VALUES (?, ?, ?)
        """,
        (parent_idea_id, child_idea_id, source_round),
    )

    conn.commit()
    conn.close()


def list_versions(parent_idea_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT child_idea_id, source_round, created_at
        FROM idea_version
        WHERE parent_idea_id = ?
        ORDER BY created_at ASC
        """,
        (parent_idea_id,),
    )

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "child_idea_id": r[0],
            "source_round": r[1],
            "created_at": r[2],
        }
        for r in rows
    ]
