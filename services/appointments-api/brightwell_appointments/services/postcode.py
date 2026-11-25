import re

_UK = re.compile(r"^([A-Z]{1,2}[0-9][A-Z0-9]?)\s*([0-9][A-Z]{2})$")


def normalise_postcode(value: str) -> str:
    v = value.strip().upper()
    m = _UK.match(v)
    if not m:
        raise ValueError("not a UK postcode")
    return f"{m.group(1)} {m.group(2)}"
