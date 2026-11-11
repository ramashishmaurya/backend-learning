"""
================================================================================
TOPIC 02: RESTFUL RESOURCES & RESOURCE NAMING CONVENTIONS
================================================================================
Run command:
    uvicorn api_mastery.topic02_resource_naming:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
GOLDEN RULES FOR RESOURCE NAMING:
1. NOUNS, NEVER VERBS:
   - ❌ BAD:  /getUsers, /createUser, /deleteOrder, /api/getData
   - ✅ GOOD: GET /users, POST /users, DELETE /orders/{id}
2. PLURAL NOUNS BY CONVENTION:
   - Use `/users`, `/products`, `/orders` (representing collections).
3. HIERARCHY & SUB-RESOURCES:
   - If resource B belongs strictly to resource A, nest it:
     `GET /users/{user_id}/orders` (orders belonging to this specific user).
     `GET /users/{user_id}/orders/{order_id}` (specific order of this user).
   - Rule of Thumb: Never nest deeper than 2 levels! Flatten complex relationships:
     `GET /reviews?order_id=45` instead of `/users/1/orders/45/items/12/reviews`.
================================================================================
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Topic 02: RESTful Resource Naming")

# In-memory stores
USERS_DB: Dict[int, dict] = {
    1: {"id": 1, "name": "Aman Verma", "email": "aman@example.com"},
    2: {"id": 2, "name": "Priya Singh", "email": "priya@example.com"}
}

ORDERS_DB: Dict[int, dict] = {
    101: {"id": 101, "user_id": 1, "item": "Mechanical Keyboard", "amount": 4500.0},
    102: {"id": 102, "user_id": 1, "item": "Wireless Mouse", "amount": 1500.0},
    103: {"id": 103, "user_id": 2, "item": "Noise Cancelling Headphones", "amount": 8999.0}
}

class User(BaseModel):
    id: int
    name: str
    email: str

class Order(BaseModel):
    id: int
    user_id: int
    item: str
    amount: float

# --- TOP-LEVEL RESOURCE: /users ---
@app.get("/users", response_model=List[User], tags=["Users Resource"])
def get_all_users():
    """Collection endpoint: Plural noun /users with GET method"""
    return list(USERS_DB.values())

@app.get("/users/{user_id}", response_model=User, tags=["Users Resource"])
def get_single_user(user_id: int):
    """Specific entity: /users/{id}"""
    user = USERS_DB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- SUB-RESOURCE: /users/{user_id}/orders ---
@app.get("/users/{user_id}/orders", response_model=List[Order], tags=["User Orders Sub-resource"])
def get_orders_for_user(user_id: int):
    """
    Sub-resource endpoint: Orders strictly belonging to a specific user.
    URI clearly expresses the parent-child relationship.
    """
    if user_id not in USERS_DB:
        raise HTTPException(status_code=404, detail="Parent user does not exist")
    
    user_orders = [o for o in ORDERS_DB.values() if o["user_id"] == user_id]
    return user_orders

# --- NON-CRUD ACTION PATTERN: /orders/{order_id}/cancel ---
@app.post("/orders/{order_id}/cancel", tags=["Actions"])
def cancel_order(order_id: int):
    """
    When an action cannot be mapped to standard CRUD (like canceling an order or checking out):
    Model it as a state-transition sub-resource action: POST /orders/{id}/cancel
    """
    order = ORDERS_DB.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["status"] = "CANCELLED"
    return {"message": f"Order {order_id} successfully cancelled"}
