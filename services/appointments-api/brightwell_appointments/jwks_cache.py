import time

import httpx

from .settings import get_settings

_cache: dict = {"at": 0.0, "keys": {}}


def keys() -> dict:
    if time.time() - _cache["at"] > 3600:
        url = get_settings().oidc.issuer + "/.well-known/jwks.json"
        _cache["keys"] = httpx.get(url, timeout=5).json()
        _cache["at"] = time.time()
    return _cache["keys"]
