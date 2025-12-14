from .base_client import BaseLLMClient


class DummyLLMClient(BaseLLMClient):
    name = "dummy"

    def generate(self, prompt: str) -> str:
        return f"[DummyLLM 输出]\n{prompt}"
