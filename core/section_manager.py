import sqlite3
from datetime import datetime
from pathlib import Path

# 与 storage.py / http_server.py 使用同一数据库
DB_PATH = Path(__file__).resolve().parent.parent / "db" / "ideaforge.db"

# 六个标准 section（中文名映射在前端，后端只认 key）
SECTIONS = [
    "product_overview",
    "users_and_scenarios",
    "functional_structure",
    "usage_flow",
    "market_and_differentiation",
    "risks_and_assumptions",
]

FINAL_SECTION_KEY = "final_definition"


def _get_conn():
    return sqlite3.connect(DB_PATH)


# ========== 初始化 ==========
def init_sections_for_idea(idea_id: int):
    """
    为 idea 初始化 6 个 section（final_definition 不在这里初始化）
    """
    conn = _get_conn()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()

    for key in SECTIONS:
        cur.execute(
            """
            INSERT OR IGNORE INTO idea_section
            (idea_id, section_key, content, status, updated_at)
            VALUES (?, ?, '', 'undefined', ?)
            """,
            (idea_id, key, now),
        )

    conn.commit()
    conn.close()


# ========== 基础读写 ==========
def get_section(idea_id: int, section_key: str):
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT idea_id, section_key, content, status, updated_at
        FROM idea_section
        WHERE idea_id = ? AND section_key = ?
        """,
        (idea_id, section_key),
    )

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "idea_id": row[0],
        "section_key": row[1],
        "content": row[2],
        "status": row[3],
        "updated_at": row[4],
    }


def upsert_section(
    idea_id: int,
    section_key: str,
    content: str,
    status: str = "stable",
):
    """
    通用写入：包括 6 个 section + final_definition
    """
    conn = _get_conn()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()

    cur.execute(
        """
        INSERT INTO idea_section
            (idea_id, section_key, content, status, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(idea_id, section_key)
        DO UPDATE SET
            content = excluded.content,
            status = excluded.status,
            updated_at = excluded.updated_at
        """,
        (idea_id, section_key, content, status, now),
    )

    conn.commit()
    conn.close()


# ========== 查询 ==========
def list_sections(idea_id: int):
    """
    只返回 6 个普通 section（不含 final_definition）
    """
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT section_key, content, status, updated_at
        FROM idea_section
        WHERE idea_id = ?
          AND section_key != ?
        ORDER BY section_key
        """,
        (idea_id, FINAL_SECTION_KEY),
    )

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "section_key": r[0],
            "content": r[1],
            "status": r[2],
            "updated_at": r[3],
        }
        for r in rows
    ]


def get_final_definition(idea_id: int):
    return get_section(idea_id, FINAL_SECTION_KEY)


def save_final_definition(idea_id: int, content: str):
    upsert_section(
        idea_id=idea_id,
        section_key=FINAL_SECTION_KEY,
        content=content,
        status="final",
    )


# ========== 报告输出 ==========
def generate_report(idea_id: int):
    """
    给前端的统一报告接口
    sections 必须是 dict，而不是 list
    """
    section_rows = list_sections(idea_id)
    final = get_final_definition(idea_id)

    sections_dict = {}
    for s in section_rows:
        sections_dict[s["section_key"]] = {
            "content": s["content"],
            "status": s["status"],
            "updated_at": s["updated_at"],
        }

    return {
        "idea_id": idea_id,
        "sections": sections_dict,   # ✅ dict，不是 list
        "final_definition": final,
        "generated_at": datetime.utcnow().isoformat(),
    }
