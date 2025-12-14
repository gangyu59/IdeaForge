from .base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    name = "PlannerAgent"

    def think(self, idea, history):
        return (
            "【项目计划草案】\n"
            "1. 明确目标与范围\n"
            "2. 核心功能拆解\n"
            "3. 技术与资源评估\n"
            "4. 时间线与里程碑\n"
            "5. 风险与对策\n"
        )
