class RelayPostError(Exception):
    def __init__(self, status: int, detail: str):
        super().__init__(f"{status}: {detail}")
        self.status = status


class RateLimited(RelayPostError):
    def __init__(self, retry_after: float):
        super().__init__(429, "rate limited")
        self.retry_after = retry_after
