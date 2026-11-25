import time

from .errors import RateLimited


def with_retry(fn, attempts: int = 3):
    for i in range(attempts):
        try:
            return fn()
        except RateLimited as exc:
            if i == attempts - 1:
                raise
            time.sleep(exc.retry_after)
