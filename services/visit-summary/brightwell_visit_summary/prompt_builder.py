from functools import lru_cache
from pathlib import Path

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "visit-summary.prompt.txt"


@lru_cache
def _template() -> str:
    return PROMPT_FILE.read_text(encoding="utf-8")


class PromptBuilder:
    def build(self, notes: str, procedure_label: str | None) -> list[dict]:
        system = _template()
        user = f"Procedure: {procedure_label or 'not recorded'}\n\nClinician notes:\n{notes}"
        return [{"role": "system", "content": system}, {"role": "user", "content": user}]
