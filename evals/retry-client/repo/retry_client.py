"""A tiny HTTP retry client used by the Ballmer Peak benchmark."""

IDEMPOTENT_METHODS = {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"}
TRANSIENT_STATUSES = {500, 502, 503, 504}


def request(transport, method, url, max_retries=2):
    """Send a request through a callable transport."""
    return transport(method, url)
