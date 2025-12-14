from .base_agent import BaseAgent
from llm_backend.llm_router import LLMRouter


class CriticAgent(BaseAgent):
    name = "CriticAgent"

    def __init__(self):
        self.llm = LLMRouter(self.name)

    def think(self, idea, history):
        prompt = (
            f"你是批判型智能体。\n"
            f"当前想法：{idea['title']}\n"
            f"历史讨论：{history}\n"
            f"请指出潜在风险和不可行点。"
        )
        return self.llm.generate(prompt)
