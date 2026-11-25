import os
from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def load_config() -> dict:
    env = os.environ.get("BW_PIPELINE_ENV", "prod")
    return yaml.safe_load((CONFIG_DIR / f"pipeline.{env}.yaml").read_text())
