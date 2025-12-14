import requests
from .base_client import BaseLLMClient
from .config import env


class GPTClient(BaseLLMClient):
    name = "gpt"

    def __init__(self):
        self.api_key = env("GPT_API_KEY")
        self.api_url = env("GPT_API_URL")
        self.model = env("GPT_MODEL", "gpt-4o")

        if not self.api_key or not self.api_url:
            raise RuntimeError("GPT config missing")

    def generate(self, prompt: str) -> str:
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json",
        }

        payload = {
            "messages": [
                {"role": "system", "content": "You are a professional AI agent."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }

        r = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()

        return data["choices"][0]["message"]["content"]
