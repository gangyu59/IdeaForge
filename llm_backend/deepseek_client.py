import requests
from .base_client import BaseLLMClient
from .config import env


class DeepSeekClient(BaseLLMClient):
    name = "deepseek"

    def __init__(self):
        self.api_key = env("DEEPSEEK_API_KEY")
        self.api_url = env("DEEPSEEK_API_URL")
        self.model = env("DEEPSEEK_MODEL")

        if not self.api_key or not self.api_url:
            raise RuntimeError("DeepSeek config missing")

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        r = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()

        return data["choices"][0]["message"]["content"]
