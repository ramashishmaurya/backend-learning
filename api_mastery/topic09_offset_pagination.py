"""
================================================================================
TOPIC 09: OFFSET-BASED PAGINATION
================================================================================
Run command:
    uvicorn api_mastery.topic09_offset_pagination:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
HOW OFFSET PAGINATION WORKS:
- Query params: `page` (1, 2, 3...) and `page_size` (e.g. 10).
- SQL formula:
    OFFSET = (page - 1) * page_size
    LIMIT = page_size
    `SELECT * FROM items ORDER BY id ASC LIMIT 10 OFFSET 20;`

THE 2 MAJOR DRAWBACKS:
1. PERFORMANCE: $O(N)$ Database scan.
   - At page 50,000, PostgreSQL must scan 500,000 rows, discard 499,990 rows,
     and return only 10 rows. Very slow on large tables!
2. PAGE DRIFT (Duplicate / Missed rows):
   - If user is on page 1, and 5 new items get inserted by other users,
     when user clicks "Next (Page 2)", the items shift down, and the user
     sees duplicate rows they already saw on page 1!
================================================================================
"""

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Generic, TypeVar

app = FastAPI(title="Topic 09: Offset Pagination")

T = TypeVar("T")

# Simulated database with 50 products
DATABASE = [{"id": i, "name": f"Product Item #{i}", "price": 100 + i * 5} for i in range(1, 51)]

class PaginationMetadata(BaseModel):
    total_records: int
    current_page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

class PaginatedResponse(BaseModel, Generic[T]):
    metadata: PaginationMetadata
    items: List[T]

@app.get("/products", response_model=PaginatedResponse[dict], tags=["Pagination"])
def get_products_offset(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page (max 50)")
):
    total_records = len(DATABASE)
    total_pages = (total_records + page_size - 1) // page_size

    offset = (page - 1) * page_size
    sliced_items = DATABASE[offset : offset + page_size]

    return PaginatedResponse(
        metadata=PaginationMetadata(
            total_records=total_records,
            current_page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        ),
        items=sliced_items
    )
