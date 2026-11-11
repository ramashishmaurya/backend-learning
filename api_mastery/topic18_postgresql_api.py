"""
================================================================================
TOPIC 18: REAL POSTGRESQL + ASYNC DRIVER (asyncpg) INTEGRATION
================================================================================
Run command:
    uvicorn api_mastery.topic18_postgresql_api:app --reload --port 8000

Visit Swagger docs:
    http://localhost:8000/docs
================================================================================
🎯 ASYNC DATABASE CONCEPTS DEMONSTRATED IN THIS FILE:
1. NON-BLOCKING I/O:
   - Every database call uses `await db.execute(...)`.
   - The Python asyncio event loop is NEVER blocked. Other requests continue to be served!
2. AUTO-TABLE MIGRATION (LIFESPAN):
   - `await conn.run_sync(Base.metadata.create_all)` runs on startup.
   - You don't need manual SQL! The tables (`users`, `products`, `orders`) are created automatically.
3. SQLALCHEMY 2.0 QUERY PATTERNS:
   - `select(Model).where(...)`: Type-safe SELECT queries.
   - `.scalar_one_or_none()`: Fetches single record or None (ideal for unique email/SKU checks).
   - `.scalars().all()`: Extracts list of ORM model objects.
   - `func.count(Model.id)`: Optimized SQL `COUNT(*)` execution.
4. REAL DATABASE PAGINATION:
   - Offset Pagination: `SELECT * FROM products ORDER BY id ASC LIMIT :size OFFSET :offset;`
   - Keyset Cursor Pagination: `SELECT * FROM products WHERE id > :cursor ORDER BY id ASC LIMIT :limit + 1;`
================================================================================
"""

import base64
import json
import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from api_mastery.database import engine, Base, get_db
from api_mastery.models import UserModel, ProductModel, OrderModel

# ------------------------------------------------------------------------------
# 1. APPLICATION LIFESPAN: ASYNC INITIALIZATION & SHUTDOWN
# ------------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan handler executes when the server starts up and shuts down.
    On Startup: Opens an async connection and creates all tables defined in models.py.
    On Shutdown: Closes all connection pools gracefully.
    """
    print("\n" + "="*70)
    print(">>> [DATABASE STARTUP] Initializing Async PostgreSQL Connection...")
    try:
        async with engine.begin() as conn:
            # `run_sync` runs synchronous DDL schema generation inside an async connection
            await conn.run_sync(Base.metadata.create_all)
        print(">>> [DATABASE SUCCESS] All PostgreSQL tables verified/created successfully!")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n>>> [DATABASE ERROR] Could not connect to PostgreSQL: {e}")
        print(">>> Check your DATABASE_URL in the .env file!\n")
    
    yield  # Application runs here and serves HTTP requests
    
    print(">>> [DATABASE SHUTDOWN] Disposing connection pool...")
    await engine.dispose()

app = FastAPI(
    title="Topic 18: Real PostgreSQL Async API",
    description="Full CRUD, real DB offset & cursor pagination, and non-blocking queries via asyncpg.",
    lifespan=lifespan
)

# ------------------------------------------------------------------------------
# 2. PYDANTIC SCHEMAS (Request & Response Validation)
# ------------------------------------------------------------------------------
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Unique corporate or personal email")
    age: int = Field(..., ge=18, le=100, description="Must be an adult (18+)")
    password: str = Field(..., min_length=6, description="Plain text password")

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read directly from SQLAlchemy ORM models!

class ProductCreate(BaseModel):
    sku: str = Field(..., min_length=3, max_length=50, description="Unique product SKU")
    title: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    category: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

class ProductResponse(BaseModel):
    id: int
    sku: str
    title: str
    category: str
    price: float
    stock: int

    class Config:
        from_attributes = True


# ------------------------------------------------------------------------------
# 3. DATABASE HEALTH CHECK ENDPOINT
# ------------------------------------------------------------------------------
@app.get("/db/health", tags=["Database Health"])
async def check_db_health(db: AsyncSession = Depends(get_db)):
    """
    Pings the PostgreSQL database with `SELECT 1` and returns round-trip latency.
    Use this to verify your `.env` connection string!
    """
    start_time = time.perf_counter()
    try:
        # Asynchronously executes raw SQL ping
        await db.execute(text("SELECT 1"))
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "status": "connected",
            "driver": "asyncpg (Asynchronous Cython PostgreSQL Driver)",
            "round_trip_latency_ms": latency_ms,
            "message": "Connection to PostgreSQL is active, pooled, and operational!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not connect to PostgreSQL database: {str(e)}"
        )


# ------------------------------------------------------------------------------
# 4. REAL DB CRUD OPERATIONS (USERS)
# ------------------------------------------------------------------------------
@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users (PostgreSQL)"],
    summary="Create user in PostgreSQL"
)
async def create_user_in_db(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    1. Runs async query: `SELECT * FROM users WHERE email = :email;`
    2. If found, raises HTTP 409 Conflict.
    3. If unique, inserts row, commits transaction, and refreshes the instance.
    """
    # Check for duplicate email in DB
    query = select(UserModel).where(UserModel.email == payload.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{payload.email}' already exists in PostgreSQL database."
        )

    # Instantiate model
    new_user = UserModel(
        name=payload.name,
        email=payload.email,
        age=payload.age,
        hashed_password=f"hashed_{payload.password}",
    )
    db.add(new_user)
    await db.commit()       # Asynchronously commits transaction to DB
    await db.refresh(new_user)  # Reloads generated columns (like id and created_at)
    return new_user


@app.get(
    "/users",
    response_model=List[UserResponse],
    tags=["Users (PostgreSQL)"],
    summary="Fetch all users from PostgreSQL"
)
async def get_all_users_from_db(db: AsyncSession = Depends(get_db)):
    """Executes: `SELECT * FROM users ORDER BY id DESC;`"""
    query = select(UserModel).order_by(UserModel.id.desc())
    result = await db.execute(query)
    return result.scalars().all()


# ------------------------------------------------------------------------------
# 5. REAL DATABASE OFFSET PAGINATION (PRODUCTS)
# ------------------------------------------------------------------------------
@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Products (PostgreSQL)"]
)
async def create_product_in_db(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    # Check duplicate SKU
    query = select(ProductModel).where(ProductModel.sku == payload.sku)
    existing = (await db.execute(query)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Product SKU already exists.")

    new_prod = ProductModel(**payload.model_dump())
    db.add(new_prod)
    await db.commit()
    await db.refresh(new_prod)
    return new_prod


@app.get(
    "/products/offset",
    tags=["Real DB Pagination"],
    summary="Real PostgreSQL Offset Pagination"
)
async def get_products_offset_from_db(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page"),
    db: AsyncSession = Depends(get_db)
):
    """
    Executes real SQL queries:
    1. Total Count: `SELECT count(products.id) FROM products;`
    2. Sliced Items: `SELECT * FROM products ORDER BY id ASC LIMIT :page_size OFFSET :offset;`
    """
    # 1. Count total records
    count_query = select(func.count(ProductModel.id))
    total_records = (await db.execute(count_query)).scalar_one()

    # 2. Query page slice
    offset = (page - 1) * page_size
    slice_query = select(ProductModel).order_by(ProductModel.id.asc()).offset(offset).limit(page_size)
    items = (await db.execute(slice_query)).scalars().all()

    total_pages = (total_records + page_size - 1) // page_size if total_records > 0 else 1

    return {
        "metadata": {
            "total_records": total_records,
            "current_page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
        "items": items
    }


# ------------------------------------------------------------------------------
# 6. REAL DATABASE CURSOR PAGINATION (KEYSET SEEK)
# ------------------------------------------------------------------------------
@app.get(
    "/products/cursor",
    tags=["Real DB Pagination"],
    summary="Real PostgreSQL Keyset Cursor Pagination"
)
async def get_products_cursor_from_db(
    cursor: Optional[str] = Query(None, description="Base64 opaque token"),
    limit: int = Query(10, ge=1, le=50, description="Items to fetch"),
    db: AsyncSession = Depends(get_db)
):
    """
    Executes real constant-time B-Tree index seek:
    `SELECT * FROM products WHERE id > :last_id ORDER BY id ASC LIMIT :limit + 1;`
    
    Why :limit + 1?
    Fetching 1 extra row tells us if another page exists WITHOUT needing an expensive `COUNT(*)` query!
    """
    last_id = 0
    if cursor:
        try:
            decoded = base64.b64decode(cursor.encode("utf-8")).decode("utf-8")
            last_id = json.loads(decoded).get("last_id", 0)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid cursor token format")

    # Fetch limit + 1 items
    query = (
        select(ProductModel)
        .where(ProductModel.id > last_id)
        .order_by(ProductModel.id.asc())
        .limit(limit + 1)
    )
    results = (await db.execute(query)).scalars().all()

    has_more = len(results) > limit
    page_items = results[:limit]

    next_cursor = None
    if has_more and page_items:
        next_id = page_items[-1].id
        next_cursor = base64.b64encode(json.dumps({"last_id": next_id}).encode("utf-8")).decode("utf-8")

    return {
        "metadata": {
            "limit": limit,
            "has_more": has_more,
            "next_cursor": next_cursor
        },
        "items": page_items
    }
