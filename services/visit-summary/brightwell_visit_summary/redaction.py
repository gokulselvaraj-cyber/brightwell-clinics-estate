"""Removes national identifiers from free-text clinician notes before they leave the service.

Only NHS numbers (10 digits, optionally 3-3-4) and Irish PPSNs (7 digits + 1-2 letters) are removed.
Names, dates of birth and addresses written into the notes are not detected (see DPIA action DP-7).
"""
import re

NHS_NUMBER = re.compile(r"\b\d{3}[ -]?\d{3}[ -]?\d{4}\b")
PPSN = re.compile(r"\b\d{7}[A-W][A-IW]?\b", re.IGNORECASE)


def strip_identifiers(text: str) -> str:
    text = NHS_NUMBER.sub("[NHS-NUMBER]", text)
    return PPSN.sub("[PPSN]", text)
