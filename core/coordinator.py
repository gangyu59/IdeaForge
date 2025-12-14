from agents.creative_agent import CreativeAgent
from agents.critic_agent import CriticAgent
from agents.refiner_agent import RefinerAgent
from agents.converger_agent import ConvergerAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.planner_agent import PlannerAgent


class Coordinator:
    def __init__(self, model: str = "dummy"):
        self.model = model
        self.brainstorm_agents = [
            CreativeAgent(),
            CriticAgent(),
            RefinerAgent(),
            ConvergerAgent(),
            EvaluatorAgent(),
        ]
        self.planner = PlannerAgent()

    def run_brainstorm(self, idea):
        history = []
        outputs = []

        for round_id, agent in enumerate(self.brainstorm_agents, start=1):
            content = agent.think(idea, history)

            outputs.append(
                {
                    "round": round_id,
                    "agent": agent.name,
                    "content": content,
                }
            )

            history.append(content)

        return outputs

    def run_planning(self, idea, history):
        content = self.planner.think(idea, history)
        return {
            "round": "planning",
            "agent": self.planner.name,
            "content": content,
        }
