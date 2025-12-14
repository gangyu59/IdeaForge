class BaseAgent:
    name = "BaseAgent"

    def think(self, idea, history):
        raise NotImplementedError
