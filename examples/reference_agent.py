"""A deterministic stand-in for a coding agent used to exercise the harness."""

from __future__ import annotations

import sys
from pathlib import Path


SOLUTION = '''"""A tiny HTTP retry client used by the Ballmer Peak benchmark."""

IDEMPOTENT_METHODS = {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"}
TRANSIENT_STATUSES = {500, 502, 503, 504}


def request(transport, method, url, max_retries=2):
    """Send a request through a callable transport."""
    attempts = max_retries + 1
    for attempt in range(attempts):
        try:
            response = transport(method, url)
        except Exception:
            if method.upper() not in IDEMPOTENT_METHODS or attempt == attempts - 1:
                raise
            continue

        if (
            method.upper() not in IDEMPOTENT_METHODS
            or response not in TRANSIENT_STATUSES
            or attempt == attempts - 1
        ):
            return response
    raise RuntimeError("request loop ended unexpectedly")
'''


def main() -> None:
    workspace = Path(sys.argv[1])
    (workspace / "retry_client.py").write_text(SOLUTION, encoding="utf-8")


if __name__ == "__main__":
    main()
