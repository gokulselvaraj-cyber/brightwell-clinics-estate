"""Loads config/clinics/*.yaml (opening hours, rooms, reminder language)."""
from functools import lru_cache
from pathlib import Path

import yaml

CLINIC_DIR = Path(__file__).resolve().parents[2] / "config" / "clinics"


@lru_cache
def load_profiles() -> dict[str, dict]:
    out = {}
    for path in sorted(CLINIC_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        out[data["code"]] = data
    return out


def reminder_language(clinic_code: str) -> str:
    return load_profiles().get(clinic_code, {}).get("reminder_language", "en-GB")
