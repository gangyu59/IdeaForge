from agents.base_agent import BaseAgent
from llm_backend.llm_router import LLMRouter


class RefinerAgent(BaseAgent):
    """
    用于：
    - Section refine
    - Final converge（最终产品定义）
    """

    name = "RefinerAgent"

    def __init__(self):
        super().__init__()
        self.router = LLMRouter(agent_name=self.name)

    def think(self, idea, history, prompt: str) -> str:
        """
        调用 LLMRouter.generate（Completion 风格）
        """
        full_prompt = (
            "你是一名资深产品经理与创业顾问。\n"
            "你的任务是将零散、分段的想法，整合为一份结构清晰、专业、可执行的产品定义文档。\n\n"
            "=== 输入内容 ===\n"
            f"{prompt}\n\n"
            "=== 输出要求 ===\n"
            "1. 使用清晰的小标题\n"
            "2. 逻辑完整、结构清楚\n"
            "3. 内容具体、避免空话\n"
            "4. 直接输出最终文档正文，不要解释\n"
        )

        return self.router.generate(full_prompt)
