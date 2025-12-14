from .base_agent import BaseAgent
from llm_backend.llm_router import LLMRouter


class CreativeAgent(BaseAgent):
    name = "CreativeAgent"

    def __init__(self):
        self.llm = LLMRouter(self.name)

    def think(self, idea, history):
        prompt = (
            f"你是创意型智能体。\n"
            f"当前想法：{idea['title']}\n"
            f"历史讨论：{history}\n"
            f"请提出新的创意方向。"
        )
        return self.llm.generate(prompt)
