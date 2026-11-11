"""
================================================================================
TOPIC 10: CURSOR-BASED (KEYSET) PAGINATION
================================================================================
Run command:
    uvicorn api_mastery.topic10_cursor_pagination:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
HOW CURSOR PAGINATION WORKS:
- Instead of counting "pages", client sends an opaque token (cursor) representing
  the last seen record's primary key or timestamp.
- SQL Equivalent:
    `SELECT * FROM items WHERE id > :last_seen_id ORDER BY id ASC LIMIT 11;`
- Why fetch 11 items if limit=10?
  If 11 rows return, we know `has_more = True` WITHOUT running an expensive `COUNT(*)`!

BENEFITS (WHY STRIPE, SLACK, TWITTER USE THIS):
1. $O(1)$ Constant Time: Direct B-Tree index seek. Blazing fast even on 50,000,000 rows.
2. Immune to Page Drift: New rows inserted or deleted do not cause duplicate reads!
================================================================================
"""

import base64
import json
from typing import Optional, List, Generic, TypeVar
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Topic 10: Cursor Pagination (Stripe/Twitter Style)")

T = TypeVar("T")

# Simulated database
DATABASE = [{"id": i, "title": f"Activity Event #{i}", "created_at": 1700000000 + i * 60} for i in range(1, 101)]

class CursorMetadata(BaseModel):
    limit: int
    has_more: bool
    next_cursor: Optional[str] = None

class CursorPaginatedResponse(BaseModel, Generic[T]):
    metadata: CursorMetadata
    items: List[T]

@app.get("/events", response_model=CursorPaginatedResponse[dict], tags=["Cursor Pagination"])
def get_events_cursor(
    cursor: Optional[str] = Query(None, description="Opaque cursor token from previous response"),
    limit: int = Query(5, ge=1, le=50, description="Number of items to fetch")
):
    last_seen_id = 0

    # 1. Decode cursor if provided
    if cursor:
        try:
            raw_json = base64.b64decode(cursor.encode("utf-8")).decode("utf-8")
            cursor_dict = json.loads(raw_json)
            last_seen_id = cursor_dict.get("last_id", 0)
        except Exception:
            raise HTTPException(status_code=400, detail="Malformed or invalid cursor token")

    # 2. SQL query equivalent: WHERE id > last_seen_id ORDER BY id ASC LIMIT limit + 1
    filtered_events = [e for e in DATABASE if e["id"] > last_seen_id]

    # Fetch limit + 1 to check if another page exists without running COUNT(*)
    slice_items = filtered_events[: limit + 1]
    has_more = len(slice_items) > limit
    page_results = slice_items[:limit]

    # 3. Generate opaque next_cursor if more items exist
    next_cursor = None
    if has_more and page_results:
        last_id = page_results[-1]["id"]
        cursor_payload = json.dumps({"last_id": last_id})
        next_cursor = base64.b64encode(cursor_payload.encode("utf-8")).decode("utf-8")

    return CursorPaginatedResponse(
        metadata=CursorMetadata(
            limit=limit,
            has_more=has_more,
            next_cursor=next_cursor
        ),
        items=page_results
    )
