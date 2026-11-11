"""
================================================================================
TOPIC 17: BACKWARD COMPATIBILITY & GRACEFUL DEPRECATION
================================================================================
Run command:
    uvicorn api_mastery.topic17_backward_compatibility:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
WHAT IS BACKWARD COMPATIBILITY?
- The ability of your backend to support older client versions without forcing
  them to update immediately.

GOLDEN RULES:
1. ADDITIVE CHANGES ARE SAFE:
   - Adding a new optional field or response attribute will NOT break existing clients.
2. BREAKING CHANGES TO AVOID:
   - Deleting a field.
   - Renaming a field (e.g. `user_name` -> `username`).
   - Changing field types (e.g. `id` from integer `12` to string `"usr_12"`).
   - Making an optional query param required.

HTTP DEPRECATION STANDARD HEADERS (RFC 8594):
- `Deprecation: true` (Signals this endpoint/param will be removed).
- `Sunset: <Date>` (Exact future date when endpoint will return 410 Gone / be shut down).
- `Warning: 299 - "..."` (Human-readable deprecation warning for developers).
================================================================================
"""

from typing import Optional
from fastapi import FastAPI, Query, Response
from pydantic import BaseModel

app = FastAPI(title="Topic 17: Backward Compatibility & Deprecation")

@app.get("/search", tags=["Backward Compatibility"])
def search_items(
    response: Response,
    q: Optional[str] = Query(None, description="[MODERN] Modern query parameter name"),
    query: Optional[str] = Query(None, description="[DEPRECATED] Old parameter name for legacy mobile apps"),
):
    """
    Demonstrates graceful migration:
    - If client sends modern parameter `q`, everything works normally.
    - If old client sends legacy `query`, we still process it, BUT we inject
      standard HTTP Deprecation and Sunset headers to notify client developers!
    """
    active_search = q

    if query and not q:
        active_search = query
        # Standard HTTP Deprecation Headers
        response.headers["Deprecation"] = "true"
        response.headers["Sunset"] = "Thu, 31 Dec 2026 23:59:59 GMT"
        response.headers["Warning"] = '299 - "Parameter \'query\' is deprecated and will be removed after 2026-12-31. Migrate to \'q\'."'

    return {
        "status": "success",
        "search_term_used": active_search or "ALL",
        "results": [
            {"id": 1, "name": f"Result for '{active_search}'"},
            {"id": 2, "name": f"Alternative result for '{active_search}'"}
        ],
        "compatibility_note": "Old and new client versions are both supported without crashing!"
    }
