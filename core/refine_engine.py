# core/refine_engine.py

from agents.creative_agent import CreativeAgent
from agents.critic_agent import CriticAgent
from agents.refiner_agent import RefinerAgent

SECTION_AGENT_MAP = {
    "product_overview": CreativeAgent,
    "users_and_scenarios": CreativeAgent,
    "functional_structure": RefinerAgent,
    "usage_flow": RefinerAgent,
    "market_and_differentiation": CriticAgent,
    "risks_and_assumptions": CriticAgent,
}


def run_refine(section_key: str, action: str, current_content: str | None):
    """
    统一返回结构：
    {
        "content": str,
        "status": "stable" | "unstable"
    }
    """

    # === 用户认可：freeze ===
    if action == "freeze":
        return {
            "content": current_content or "",
            "status": "stable"
        }

    # === 其它操作：生成 / 质疑 ===
    if action == "deepen":
        AgentClass = CreativeAgent
    elif action == "challenge":
        AgentClass = CriticAgent
    else:
        raise ValueError(f"Unknown refine action: {action}")

    agent = AgentClass()

    idea = {
        "title": section_key
    }

    history = current_content or ""

    result = agent.think(idea, history)

    if not isinstance(result, str):
        raise TypeError(
            f"{agent.__class__.__name__}.think() must return str, got {type(result)}"
        )

    return {
        "content": result.strip(),
        "status": "unstable"
    }



