from dataclasses import dataclass


@dataclass
class Message:
    message_id: str
    status: str
    segments: int
