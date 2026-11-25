import os
from pathlib import Path

import yaml

CONFIG = Path(__file__).resolve().parent.parent / "config" / "application.yml"


def load() -> dict:
    cfg = yaml.safe_load(os.path.expandvars(CONFIG.read_text()))
    cfg["database"]["host"] = os.environ.get("DB_HOST", cfg["database"]["host"])
    cfg["database"]["port"] = int(os.environ.get("DB_PORT", cfg["database"]["port"]))
    return cfg
