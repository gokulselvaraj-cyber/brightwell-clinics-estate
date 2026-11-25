import httpx

from .errors import RateLimited, RelayPostError
from .models import Message
from .retry import with_retry


class RelayPostClient:
    def __init__(self, base_url: str = "https://api.relaypost.example/v2", api_key: str = "",
                 timeout: float = 10.0):
        self._http = httpx.Client(base_url=base_url, timeout=timeout,
                                  headers={"Authorization": f"Key {api_key}"})

    def send_message(self, to: str, sender: str, body: str) -> Message:
        def call():
            r = self._http.post("/messages", json={"to": to, "from": sender, "body": body})
            if r.status_code == 429:
                raise RateLimited(float(r.headers.get("Retry-After", "1")))
            if r.status_code >= 400:
                raise RelayPostError(r.status_code, r.text[:200])
            j = r.json()
            return Message(j["id"], j["status"], j.get("segments", 1))
        return with_retry(call)

    def message_status(self, message_id: str) -> str:
        r = self._http.get(f"/messages/{message_id}")
        r.raise_for_status()
        return r.json()["status"]
