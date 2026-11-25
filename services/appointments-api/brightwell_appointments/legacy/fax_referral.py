"""Fax referral intake (2019). Parsed referral letters dropped by the fax-to-email box into
/srv/fax-inbox. Superseded by e-referrals in 2023; nothing imports this module any more."""
import re
from pathlib import Path

INBOX = Path("/srv/fax-inbox")
_NHS = re.compile(r"NHS\s*No[:.]?\s*(\d{3}\s?\d{3}\s?\d{4})")


class FaxReferralParser:
    def parse(self, text: str) -> dict:
        m = _NHS.search(text)
        return {"nhs_number": m.group(1).replace(" ", "") if m else None,
                "urgent": "URGENT" in text.upper(), "raw": text[:2000]}

    def poll(self) -> list[dict]:
        return [self.parse(p.read_text(errors="replace")) for p in sorted(INBOX.glob("*.txt"))]
