from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"


def template_for(nation: str) -> str:
    return {"IE": "reminder_sms_ie.j2", "WAL": "reminder_sms_cy.j2"}.get(nation, "reminder_sms.j2")
