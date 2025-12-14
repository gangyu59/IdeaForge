from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# ===== core imports =====
from core.idea_manager import create_idea
from core.coordinator import Coordinator
from core.storage import save_agent_outputs, load_agent_outputs
from core.state_manager import update_idea_status, get_idea_status
from core.fork_manager import fork_idea
from core.version_manager import list_versions
from core.refine_engine import run_refine

from core.section_manager import (
    init_sections_for_idea,
    get_section,
    upsert_section,
    list_sections,
    save_final_definition,
    get_final_definition,
    generate_report,
)


# =======================
# FastAPI app (ONLY ONCE)
# =======================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",
        "http://127.0.0.1:63342",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = Coordinator()

# =======================
# Pydantic Models
# =======================

class IdeaIn(BaseModel):
    title: str
    description: str


class RefineRequest(BaseModel):
    section: str
    action: str   # deepen | challenge | freeze
    hint: str = ""

# =======================
# Idea APIs
# =======================

@app.post("/idea")
def create_idea_api(data: IdeaIn):
    idea_id = create_idea(data.title, data.description)

    # 初始化 6 个 section（关键）
    init_sections_for_idea(idea_id)

    return {
        "idea_id": idea_id,
        "status": "draft"
    }


@app.post("/idea/{idea_id}/brainstorm")
def brainstorm(idea_id: int):
    status = get_idea_status(idea_id)

    if status in ("converged", "planning"):
        raise HTTPException(
            status_code=400,
            detail=f"Brainstorm already completed, status={status}",
        )

    idea = {"id": idea_id, "title": f"Idea-{idea_id}"}

    outputs = coordinator.run_brainstorm(idea)

    save_agent_outputs(idea_id, outputs)
    update_idea_status(idea_id, "converged")

    return outputs


@app.get("/idea/{idea_id}/result")
def get_result(idea_id: int):
    results = load_agent_outputs(idea_id)

    if not results:
        raise HTTPException(status_code=404, detail="No discussion found")

    status = get_idea_status(idea_id)

    return {
        "idea_id": idea_id,
        "status": status,
        "discussion": results,
        "final_summary": results[-1]["content"],
    }


@app.post("/idea/{idea_id}/initiate")
def initiate_project(idea_id: int):
    status = get_idea_status(idea_id)

    if status != "converged":
        raise HTTPException(
            status_code=400,
            detail=f"Idea status must be converged, current={status}",
        )

    history = load_agent_outputs(idea_id)
    idea = {"id": idea_id, "title": f"Idea-{idea_id}"}

    plan = coordinator.run_planning(idea, history)

    save_agent_outputs(idea_id, [plan])
    update_idea_status(idea_id, "planning")

    return {
        "idea_id": idea_id,
        "status": "planning",
        "plan": plan,
    }


@app.post("/idea/{idea_id}/fork")
def fork_idea_api(idea_id: int, source_round: str = "final"):
    try:
        child_id = fork_idea(idea_id, source_round)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "parent_idea_id": idea_id,
        "child_idea_id": child_id,
        "source_round": source_round,
        "status": "draft",
    }


@app.get("/idea/{idea_id}/versions")
def list_idea_versions(idea_id: int):
    return {
        "parent_idea_id": idea_id,
        "versions": list_versions(idea_id),
    }

# =======================
# Section Refinement APIs
# =======================

@app.post("/idea/{idea_id}/refine")
def refine_section(idea_id: int, req: RefineRequest):
    section = get_section(idea_id, req.section)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    # 🚨 如果已认可，禁止任何再次修改
    if section["status"] == "stable" and req.action != "freeze":
        return {
            "section": req.section,
            "content": section["content"],
            "status": "stable",
        }

    # ===== freeze：只做一次性固化 =====
    if req.action == "freeze":
        upsert_section(
            idea_id=idea_id,
            section_key=req.section,
            content=section["content"],
            status="stable",
        )
        return {
            "section": req.section,
            "content": section["content"],
            "status": "stable",
        }

    # ===== 其它操作（只允许 unstable 时） =====
    result = run_refine(
        section_key=req.section,
        action=req.action,
        current_content=section["content"],
    )

    if not isinstance(result, dict):
        raise HTTPException(status_code=500, detail="Invalid refine result")

    upsert_section(
        idea_id=idea_id,
        section_key=req.section,
        content=result["content"],
        status="unstable",
    )

    return {
        "section": req.section,
        "content": result["content"],
        "status": "unstable",
    }


@app.get("/idea/{idea_id}/report")
def get_idea_report(idea_id: int):
    """
    返回 6 个 section + final_definition（如果存在）
    """
    return generate_report(idea_id)



from datetime import datetime
from fastapi import HTTPException
from core.section_manager import upsert_section, list_sections
from core.refine_engine import run_refine


@app.post("/idea/{idea_id}/converge")
def converge_idea(idea_id: int):
    """
    生成并持久化最终产品定义（真实调用 LLM）
    """
    sections = list_sections(idea_id)
    if not sections:
        raise HTTPException(status_code=400, detail="No sections to converge")

    prompt_parts = []
    for s in sections:
        if not s["content"]:
            continue
        prompt_parts.append(
            f"### {s['section_key']}\n{s['content']}"
        )

    if not prompt_parts:
        raise HTTPException(status_code=400, detail="All sections are empty")

    prompt = (
        "请基于以下六个部分，生成一份完整、专业、可直接用于立项评审的【最终产品定义文档】。\n\n"
        "要求：\n"
        "1. 使用清晰的标题与层级结构\n"
        "2. 内容必须具体、可执行\n"
        "3. 不要简单复述原文，要进行整合、提炼与升级\n\n"
        + "\n\n".join(prompt_parts)
    )

    from agents.refiner_agent import RefinerAgent
    agent = RefinerAgent()

    final_content = agent.think(
        idea={"id": idea_id},
        history=[],
        prompt=prompt,
    )

    if not final_content:
        raise HTTPException(status_code=500, detail="LLM returned empty result")

    save_final_definition(idea_id, final_content)

    return {
        "idea_id": idea_id,
        "status": "ok",
        "final_summary": final_content,
    }
