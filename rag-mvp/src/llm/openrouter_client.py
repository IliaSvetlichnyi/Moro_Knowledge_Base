import httpx
from src.config import settings


class OpenRouterClient:
    def __init__(self):
        self.base = settings.OPENROUTER_BASE_URL.rstrip("/")
        self.key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

    def chat(self, system: str, user: str, max_new_tokens: int, temperature: float) -> str:
        url = f"{self.base}/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_tokens": max_new_tokens,
            "stream": False,
        }
        with httpx.Client(timeout=60) as client:
            resp = client.post(url, headers=self.headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

