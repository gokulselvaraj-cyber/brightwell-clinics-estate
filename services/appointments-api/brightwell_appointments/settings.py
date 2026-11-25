"""Typed settings. YAML from config/ is layered: application.yml, then application-<BW_ENV>.yml,
then BW_* environment variables."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    name: str = "appointmentsdb"
    user: str = "bw_app"
    password: str = ""
    pool_size: int = 10


class BookingSettings(BaseModel):
    # Hours before the start time after which a cancellation counts as late (fee + no-show risk).
    late_cancel_hours: int = 24
    max_future_days: int = 120
    hold_minutes: int = 10


class ReminderSettings(BaseModel):
    offsets_hours: list[int] = [48, 2]
    channel: str = "SMS"


class VisitSummarySettings(BaseModel):
    url: str = "http://localhost:8070"
    timeout_seconds: int = 20


class OidcSettings(BaseModel):
    issuer: str = "https://login.brightwell.internal"
    audience: str = "appointments-api"
    client_secret: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BW_", env_nested_delimiter="__")
    env: str = "dev"
    database: DatabaseSettings = DatabaseSettings()
    booking: BookingSettings = BookingSettings()
    reminders: ReminderSettings = ReminderSettings()
    visit_summary: VisitSummarySettings = VisitSummarySettings()
    oidc: OidcSettings = OidcSettings()


def _load_yaml(name: str) -> dict:
    path = CONFIG_DIR / name
    if not path.exists():
        return {}
    text = os.path.expandvars(path.read_text(encoding="utf-8"))
    return yaml.safe_load(text) or {}


def _merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for key, value in over.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = value
    return out


@lru_cache
def get_settings() -> Settings:
    env = os.environ.get("BW_ENV", "dev")
    data = _merge(_load_yaml("application.yml"), _load_yaml(f"application-{env}.yml"))
    data.pop("server", None)
    # The cluster ConfigMaps (infra/k8s/overlays/<env>) set VISIT_SUMMARY_URL; it wins over YAML.
    if os.environ.get("VISIT_SUMMARY_URL"):
        data.setdefault("visit_summary", {})["url"] = os.environ["VISIT_SUMMARY_URL"]
    return Settings(env=env, **data)
