import sqlite3
from pathlib import Path

from core.idea_manager import create_idea
from core.storage import load_agent_outputs
from core.version_manager import create_version

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "ideaforge.db"


def fork_idea(parent_idea_id: int, source_round: str = "final") -> int:
    """
    source_round:
      - 数字字符串：'1'...'5'
      - 'final'：使用最终摘要
    """
    history = load_agent_outputs(parent_idea_id)
    if not history:
        raise ValueError("Parent idea has no discussion")

    if source_round == "final":
        base_content = history[-1]["content"]
    else:
        round_no = int(source_round)
        matched = [h for h in history if h["round"] == round_no]
        if not matched:
            raise ValueError(f"Round {source_round} not found")
        base_content = matched[0]["content"]

    title = f"Fork of Idea-{parent_idea_id}"
    description = f"Forked from Idea-{parent_idea_id}, source_round={source_round}\n\n{base_content}"

    child_idea_id = create_idea(title, description)
    create_version(parent_idea_id, child_idea_id, source_round)

    return child_idea_id
