"""
================================================================================
TOPIC 14: RATE LIMITING & SLIDING WINDOW COUNTERS
================================================================================
Run command:
    uvicorn api_mastery.topic14_rate_limiting:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
WHY RATE LIMITING?
- Protects downstream database / LLM services from being overloaded.
- Defends against brute-force password guessing and scraping bots.

ALGORITHMS:
1. Token Bucket: Fixed refill rate. Permits short bursts.
2. Leaky Bucket: Smooth, constant queue output.
3. Sliding Window Log/Counter: Tracks timestamps within a rolling window [now - window, now].
   Prevents the "Double Burst" bug at fixed boundary edges.

STANDARD HTTP HEADERS:
- `X-RateLimit-Limit`: Maximum requests allowed in window.
- `X-RateLimit-Remaining`: Remaining quota in this window.
- `X-RateLimit-Reset`: Unix timestamp when quota resets.
- `Retry-After`: Seconds to wait before retrying (sent with 429 Too Many Requests).
================================================================================
"""

import time
import json
from typing import Dict, List
from fastapi import FastAPI, Request, Response, status

app = FastAPI(title="Topic 14: Sliding Window Rate Limiting")

# Simulated storage: IP address -> list of request timestamps
RATE_LIMIT_STORE: Dict[str, List[float]] = {}

WINDOW_SECONDS = 10  # 10-second rolling window
MAX_REQUESTS = 5    # Max 5 requests allowed per 10 seconds

@app.middleware("http")
async def sliding_window_rate_limiter(request: Request, call_next):
    # Only limit /api/ routes
    if not request.url.path.startswith("/api/"):
        return await call_next(request)

    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.time()

    # 1. Slide window: Filter out timestamps older than (now - WINDOW_SECONDS)
    history = RATE_LIMIT_STORE.get(client_ip, [])
    valid_window_history = [t for t in history if now - t < WINDOW_SECONDS]

    # 2. Check if quota exceeded
    if len(valid_window_history) >= MAX_REQUESTS:
        oldest_ts = valid_window_history[0]
        retry_after = int(WINDOW_SECONDS - (now - oldest_ts)) + 1
        return Response(
            content=json.dumps({
                "error": "Too Many Requests",
                "message": f"Rate limit exceeded. Maximum {MAX_REQUESTS} requests per {WINDOW_SECONDS}s.",
                "retry_after_seconds": retry_after
            }),
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            media_type="application/json",
            headers={
                "Retry-After": str(retry_after),
                "X-RateLimit-Limit": str(MAX_REQUESTS),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(now + retry_after))
            }
        )

    # 3. Add current timestamp
    valid_window_history.append(now)
    RATE_LIMIT_STORE[client_ip] = valid_window_history

    # 4. Proceed and append rate limit headers to response
    response = await call_next(request)
    remaining = MAX_REQUESTS - len(valid_window_history)
    response.headers["X-RateLimit-Limit"] = str(MAX_REQUESTS)
    response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
    response.headers["X-RateLimit-Reset"] = str(int(now + WINDOW_SECONDS))
    return response

@app.get("/api/data", tags=["Rate Limited Resource"])
def get_resource():
    """Try refreshing this endpoint 6 times rapidly in Swagger to trigger HTTP 429!"""
    return {"message": "Success! You have valid quota."}
