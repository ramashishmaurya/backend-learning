"""
================================================================================
TOPIC 03: HTTP METHODS (VERBS) — SAFE VS IDEMPOTENT
================================================================================
Run command:
    uvicorn api_mastery.topic03_http_methods:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
INTERVIEW DEFINITIONS:
1. SAFE METHODS:
   - Does NOT change server state. Calling it 100 times has zero side effects.
   - Examples: GET, HEAD, OPTIONS.
2. IDEMPOTENT METHODS:
   - Calling the method 1 time has the EXACT SAME effect on the server as calling it 100 times.
   - Examples: PUT (overwrites whole entity), DELETE (deletes entity), GET.
3. NON-IDEMPOTENT METHODS:
   - Calling it 10 times produces 10 different effects!
   - Example: POST (creates 10 different orders or charges card 10 times).
4. PUT vs PATCH:
   - PUT: Full replacement. Client must send all fields.
   - PATCH: Partial modification. Client sends only fields that need changing.
================================================================================
"""

from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI(title="Topic 03: HTTP Methods Deep-Dive")

PRODUCTS: Dict[int, dict] = {
    1: {"id": 1, "title": "MacBook Air", "price": 99999.0, "stock": 10}
}

class ProductCreate(BaseModel):
    title: str
    price: float
    stock: int

class ProductFullReplace(BaseModel):
    title: str
    price: float
    stock: int

class ProductPartialUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

# 1. GET: Safe and Idempotent
@app.get("/products/{prod_id}", tags=["HTTP Methods"])
def get_product(prod_id: int):
    """SAFE & IDEMPOTENT: Reads data without changing server state."""
    prod = PRODUCTS.get(prod_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

# 2. POST: Neither Safe nor Idempotent
@app.post("/products", status_code=status.HTTP_201_CREATED, tags=["HTTP Methods"])
def create_product(payload: ProductCreate):
    """NOT SAFE & NOT IDEMPOTENT: Every request creates a brand new record."""
    new_id = len(PRODUCTS) + 1
    new_item = {"id": new_id, **payload.model_dump()}
    PRODUCTS[new_id] = new_item
    return new_item

# 3. PUT: Full Replacement (Idempotent)
@app.put("/products/{prod_id}", tags=["HTTP Methods"])
def full_replace_product(prod_id: int, payload: ProductFullReplace):
    """
    IDEMPOTENT: Full replacement.
    If you send this 10 times with the same body, the final DB state remains identical.
    """
    if prod_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Replaces entire object
    PRODUCTS[prod_id] = {"id": prod_id, **payload.model_dump()}
    return {"message": "Resource fully replaced", "product": PRODUCTS[prod_id]}

# 4. PATCH: Partial Update
@app.patch("/products/{prod_id}", tags=["HTTP Methods"])
def partial_update_product(prod_id: int, payload: ProductPartialUpdate):
    """
    PARTIAL UPDATE: Modifies only fields explicitly sent.
    """
    if prod_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    PRODUCTS[prod_id].update(update_data)
    return {"message": "Resource partially updated", "product": PRODUCTS[prod_id]}

# 5. DELETE: Remove Resource (Idempotent)
@app.delete("/products/{prod_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["HTTP Methods"])
def delete_product(prod_id: int):
    """
    IDEMPOTENT: Deletes resource.
    First call deletes it. Successive calls still leave the item deleted.
    Returns 204 No Content (No response body).
    """
    if prod_id in PRODUCTS:
        del PRODUCTS[prod_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
