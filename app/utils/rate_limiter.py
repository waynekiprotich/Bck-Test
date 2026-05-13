from collections import defaultdict
from time import time

# In-memory store: {key: [timestamps]}
# NOTE: This resets on server restart.
# Good enough for MVP — upgrade to Redis in production if needed.
_store = defaultdict(list)


def rate_limit(key: str, max_calls: int = 10, window_seconds: int = 60) -> bool:
    """
    Check if a key has exceeded its rate limit.

    Returns True  → limit exceeded, reject the request.
    Returns False → within limit, allow the request.

    Example:
        if rate_limit(f"submit:{user_id}", max_calls=10, window_seconds=60):
            return jsonify({"error": "Too many submissions"}), 429
    """
    now = time()

    # Drop timestamps that have slid outside the window
    _store[key] = [t for t in _store[key] if now - t < window_seconds]

    if len(_store[key]) >= max_calls:
        return True  # limit exceeded

    _store[key].append(now)
    return False  # within limit
