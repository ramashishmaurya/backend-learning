"""
================================================================================
TOPIC 11: FILTERING, SORTING & SEARCHING
================================================================================
Run command:
    uvicorn api_mastery.topic11_filtering_sorting_searching:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
PATTERNS:
1. FILTERING: Use query params matching attributes:
   - `?category=Electronics&min_price=500&max_price=2000`
2. SEARCHING: Free-text search parameter:
   - `?q=wireless` (searches across title, description, tags)
3. SORTING: Support flexible column sorting:
   - `?sort_by=price&order=desc` OR comma-separated syntax `?sort=-price,title`
================================================================================
"""

from typing import Optional, List
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Topic 11: Filtering, Sorting & Searching")

CATALOG = [
    {"id": 1, "title": "Logitech Wireless Mouse", "category": "Electronics", "price": 1299.0, "rating": 4.5},
    {"id": 2, "title": "Mechanical Gaming Keyboard", "category": "Electronics", "price": 4999.0, "rating": 4.8},
    {"id": 3, "title": "Clean Code by Robert Martin", "category": "Books", "price": 799.0, "rating": 4.9},
    {"id": 4, "title": "Designing Data-Intensive Apps", "category": "Books", "price": 1850.0, "rating": 5.0},
    {"id": 5, "title": "Ergonomic Office Chair", "category": "Furniture", "price": 12500.0, "rating": 4.2},
    {"id": 6, "title": "Adjustable Standing Desk", "category": "Furniture", "price": 24000.0, "rating": 4.7},
]

class SearchResult(BaseModel):
    total_found: int
    applied_filters: dict
    items: List[dict]

@app.get("/catalog/search", response_model=SearchResult, tags=["Querying"])
def search_catalog(
    q: Optional[str] = Query(None, description="Search keyword in title"),
    category: Optional[str] = Query(None, description="Exact category match"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    sort_by: str = Query("id", pattern="^(id|price|rating|title)$", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order: asc or desc"),
):
    results = CATALOG.copy()

    # 1. FILTERING: Category & Price Bounds
    if category:
        results = [p for p in results if p["category"].lower() == category.lower()]
    if min_price is not None:
        results = [p for p in results if p["price"] >= min_price]
    if max_price is not None:
        results = [p for p in results if p["price"] <= max_price]

    # 2. SEARCHING: Keyword lookup
    if q:
        query_word = q.strip().lower()
        results = [p for p in results if query_word in p["title"].lower()]

    # 3. SORTING: Dynamic sort
    reverse = (order.lower() == "desc")
    results = sorted(results, key=lambda x: x[sort_by], reverse=reverse)

    return SearchResult(
        total_found=len(results),
        applied_filters={
            "q": q,
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "sort_by": sort_by,
            "order": order
        },
        items=results
    )
