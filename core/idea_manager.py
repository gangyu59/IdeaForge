import sqlite3

DB = "db/ideaforge.db"

def create_idea(title, description):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO idea (title, description, status) VALUES (?, ?, ?)",
        (title, description, "draft")
    )
    conn.commit()
    return cur.lastrowid
