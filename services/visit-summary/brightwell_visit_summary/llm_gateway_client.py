"""Client for the Brightwell LLM gateway (OpenAI-compatible chat completions API)."""
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .settings import get_settings


class LlmGatewayClient:
    def __init__(self):
        self.cfg = get_settings()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=8))
    def complete(self, messages: list[dict]) -> str:
        resp = httpx.post(self.cfg.llm_gateway_url, timeout=self.cfg.llm_timeout_seconds,
                          headers={"Authorization": f"Bearer {self.cfg.llm_gateway_token}",
                                   "X-BW-Purpose": "visit-summary"},
                          json={"model": self.cfg.llm_model, "messages": messages,
                                "max_tokens": self.cfg.llm_max_tokens,
                                "temperature": self.cfg.llm_temperature})
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
