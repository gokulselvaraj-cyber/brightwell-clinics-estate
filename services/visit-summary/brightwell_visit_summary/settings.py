from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_gateway_url: str = "https://llm-gateway.brightwell.internal/v1/chat/completions"
    llm_gateway_token: str = ""          # from env LLM_GATEWAY_TOKEN (Secrets Manager)
    llm_model: str = "bw-clinsum-2"
    llm_max_tokens: int = 700
    llm_temperature: float = 0.2
    llm_timeout_seconds: int = 25
    visit_summary_llm_enabled: bool = True
    archive_bucket: str = "bw-visit-summaries-euw2"
    archive_region: str = "eu-west-2"
    database_url: str = "postgresql+psycopg://bw_summary@localhost:5432/appointmentsdb"
    port: int = 8070


@lru_cache
def get_settings() -> Settings:
    return Settings()
