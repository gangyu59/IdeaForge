from llm_backend.policy import AGENT_MODEL_POLICY
from llm_backend.dummy_client import DummyLLMClient
from llm_backend.gpt_client import GPTClient
from llm_backend.deepseek_client import DeepSeekClient
from llm_backend.ark_client import ArkClient


class LLMRouter:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        policy = AGENT_MODEL_POLICY.get(agent_name, {})
        self.primary = policy.get("primary", "dummy")
        self.fallback = policy.get("fallback", "dummy")

    def _load_client(self, provider: str):
        if provider == "gpt":
            return GPTClient()
        if provider == "deepseek":
            return DeepSeekClient()
        if provider in ("ark", "doubao"):
            return ArkClient()
        return DummyLLMClient()

    def generate(self, prompt: str) -> str:
        try:
            return self._load_client(self.primary).generate(prompt)
        except Exception as e:
            print(
                f"[LLMRouter] {self.agent_name} primary={self.primary} failed: {e}"
            )
            return self._load_client(self.fallback).generate(prompt)
