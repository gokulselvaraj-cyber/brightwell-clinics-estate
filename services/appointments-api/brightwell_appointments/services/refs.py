import secrets

_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def new_appointment_ref() -> str:
    """BWA- plus 10 characters, no I/O/0/1 so they can be read over the phone."""
    return "BWA-" + "".join(secrets.choice(_ALPHABET) for _ in range(10))
