from __future__ import annotations
from time import monotonic, sleep
from urllib.parse import urlparse

class EgressViolation(RuntimeError):
    pass

class RateLimiter:
    def __init__(self, rpm: int):
        self.rpm = max(1, rpm)
        self._last = 0.0
    def wait(self) -> None:
        interval = 60.0 / self.rpm
        now = monotonic()
        delta = now - self._last
        if delta < interval:
            sleep(interval - delta)
        self._last = monotonic()

def assert_egress_allowed(url: str, allowed_domains: list[str]) -> None:
    host = (urlparse(url).hostname or "").lower()
    allowed = [d.lower() for d in allowed_domains]
    if not any(host == d or host.endswith("." + d) for d in allowed):
        raise EgressViolation(f"Destino fora da allowlist: {host}; permitidos={allowed_domains}")
