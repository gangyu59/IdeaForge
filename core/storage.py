import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "ideaforge.db"


def save_agent_outputs(idea_id: int, outputs: list[dict]):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for item in outputs:
        cur.execute(
            """
            INSERT INTO agent_output (idea_id, round, agent_name, content)
            VALUES (?, ?, ?, ?)
            """,
            (
                idea_id,
                item["round"],
                item["agent"],
                item["content"],
            ),
        )

    conn.commit()
    conn.close()


def load_agent_outputs(idea_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT round, agent_name, content
        FROM agent_output
        WHERE idea_id = ?
        ORDER BY round ASC
        """,
        (idea_id,),
    )

    rows = cur.fetchall()
    conn.close()

    return [
        {"round": r[0], "agent": r[1], "content": r[2]}
        for r in rows
    ]


def has_agent_outputs(idea_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM agent_output WHERE idea_id = ?",
        (idea_id,),
    )
    count = cur.fetchone()[0]

    conn.close()
    return count > 0
