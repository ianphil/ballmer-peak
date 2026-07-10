"""External grader for the retry-client benchmark."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load_candidate(workspace: Path):
    spec = importlib.util.spec_from_file_location(
        "retry_client_candidate", workspace / "retry_client.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load candidate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Transport:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.calls = 0

    def __call__(self, method, url):
        self.calls += 1
        outcome = next(self.outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def check(name, function):
    try:
        function()
        return True, name
    except Exception as error:
        return False, f"{name}: {error}"


def main() -> None:
    candidate = load_candidate(Path(sys.argv[1]))
    cases = []

    def retries_transient_get():
        transport = Transport([503, 200])
        assert candidate.request(transport, "GET", "/", 2) == 200
        assert transport.calls == 2

    cases.append(check("retries transient GET", retries_transient_get))

    def avoids_retrying_post():
        transport = Transport([503, 200])
        assert candidate.request(transport, "POST", "/", 2) == 503
        assert transport.calls == 1

    cases.append(check("does not retry POST", avoids_retrying_post))

    def returns_non_transient_response():
        transport = Transport([404, 200])
        assert candidate.request(transport, "GET", "/", 2) == 404
        assert transport.calls == 1

    cases.append(check("returns non-transient response", returns_non_transient_response))

    def respects_retry_limit():
        transport = Transport([500, 502, 503, 200])
        assert candidate.request(transport, "GET", "/", 2) == 503
        assert transport.calls == 3

    cases.append(check("respects max_retries", respects_retry_limit))

    def retries_transport_exception():
        transport = Transport([OSError("network"), 200])
        assert candidate.request(transport, "HEAD", "/", 1) == 200
        assert transport.calls == 2

    cases.append(check("retries transport exception", retries_transport_exception))

    passed = sum(success for success, _ in cases)
    print(
        json.dumps(
            {
                "passed": passed,
                "total": len(cases),
                "details": [detail for _, detail in cases],
            }
        )
    )


if __name__ == "__main__":
    main()
