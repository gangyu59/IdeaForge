class BaseLLMClient:
    name = "base"

    def generate(self, prompt: str) -> str:
        raise NotImplementedError
