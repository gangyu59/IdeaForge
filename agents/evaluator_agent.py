from .base_agent import BaseAgent

class EvaluatorAgent(BaseAgent):
    name = "EvaluatorAgent"

    def think(self, idea, history):
        return "综合各方意见，给出是否值得推进的结论。"
