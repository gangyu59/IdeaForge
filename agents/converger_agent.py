from .base_agent import BaseAgent


class ConvergerAgent(BaseAgent):
    name = "ConvergerAgent"

    def think(self, idea, history):
        return (
            "对多个改进方向进行取舍，明确一个最值得推进的核心方案，"
            "并说明选择理由。"
        )
