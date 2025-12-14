import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "ideaforge.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            sql = f.read()
        conn.executescript(sql)
        conn.commit()
        print(f"✅ 数据库已初始化: {DB_PATH}")
    except Exception as e:
        print("❌ 执行 schema.sql 失败：")
        print(e)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
