"""
================================================================================
TOPIC 07: API VERSIONING STRATEGIES
================================================================================
Run command:
    uvicorn api_mastery.topic07_api_versioning:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
WHY VERSIONING?
- When you release mobile apps on the App Store / Play Store, users don't update immediately.
- If you change a response from `{"name": "Aman"}` to `{"first_name": "Aman", "last_name": "Kumar"}`,
  old mobile apps will CRASH!
- Versioning allows old clients to continue calling `/api/v1` while new web clients use `/api/v2`.
================================================================================
"""

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Topic 07: API Versioning (v1 vs v2)")

# Shared Database Simulation
MOCK_DATABASE = [
    {"id": 1, "first_name": "Amitabh", "last_name": "Bachchan", "email": "amitabh@example.com"}
]

# --- VERSION 1 CONTRACT (Old Single Name Field) ---
class UserV1(BaseModel):
    id: int
    name: str  # Combines first and last name
    email: str

v1_router = APIRouter(prefix="/api/v1", tags=["API Version 1"])

@v1_router.get("/users", response_model=List[UserV1])
def get_users_v1():
    """V1: Returns legacy 'name' field for older mobile clients"""
    return [
        {
            "id": u["id"],
            "name": f"{u['first_name']} {u['last_name']}",
            "email": u["email"]
        }
        for u in MOCK_DATABASE
    ]

# --- VERSION 2 CONTRACT (New Granular Fields) ---
class UserV2(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

v2_router = APIRouter(prefix="/api/v2", tags=["API Version 2"])

@v2_router.get("/users", response_model=List[UserV2])
def get_users_v2():
    """V2: Returns separate 'first_name' and 'last_name' for modern web clients"""
    return MOCK_DATABASE

# Mount both routers onto application
app.include_router(v1_router)
app.include_router(v2_router)
