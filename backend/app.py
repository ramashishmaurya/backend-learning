from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models import UserModel, ProductModel, OrderModel

app = FastAPI(
    title="Backend Learning API",
    summary="Connected to PostgreSQL 'design' database"
)


# ==============================================================================
# PYDANTIC SCHEMAS FOR DATABASE OPERATIONS
# ==============================================================================
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=18, le=100)
    password: str = Field(..., min_length=6)



class updateinformation(BaseModel) :

    name : str




class ProductResponse(BaseModel):
    id: int
    sku: str
    title: str
    category: str
    price: float
    stock: int
    is_active: bool

    class Config:
        from_attributes = True


# ==============================================================================
# 1. LIVE DATABASE HEALTH CHECK
# ==============================================================================
@app.get("/db/health", tags=["Database"])
async def check_database_health(db: AsyncSession = Depends(get_db)):
    """Pings PostgreSQL to verify live connection to 'design' DB."""
    try:
        result = await db.execute(text("SELECT current_database(), count(*) FROM products;"))
        row = result.fetchone()
        return {
            "status": "connected",
            "database": row[0],
            "total_products_in_db": row[1],
            "message": "Successfully connected to PostgreSQL 'design' database!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


# ==============================================================================
# 2. USERS OPERATIONS ON ACTUAL DATABASE
# ==============================================================================
@app.get("/db/users", response_model=List[UserResponse], tags=["Users (PostgreSQL)"])
async def get_all_users(
    limit: int = Query(10, ge=1, le=50, description="Kitne users fetch karne hain (Default 10)"), # this line for limit right 
    db: AsyncSession = Depends(get_db)
):
    """Fetches users from the 'users' table in 'design' database."""
    query = select(UserModel).order_by(UserModel.id.asc()).limit(limit)   
    result = await db.execute(query)
    return result.scalars().all()


@app.post("/db/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users (PostgreSQL)"])
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    """Inserts a new user into the actual 'users' table."""
    # Check duplicate email
    existing = (await db.execute(select(UserModel).where(UserModel.email == payload.email))).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail=f"User with email '{payload.email}' already exists.")

    new_user = UserModel(
        name=payload.name,
        email=payload.email,
        age=payload.age,
        hashed_password=f"hashed_{payload.password}"   
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@app.patch("/db/users/{user_id}" , 
           response_model=UserResponse , 
           status_code=status.HTTP_200_OK , 
           tags=['users(postgres sql)'])
async def update_user_name(
    user_id: int,
    payload: updateinformation, 
    db: AsyncSession = Depends(get_db)
):

    result  = await db.execute(
        select(UserModel).where(UserModel.id ==user_id)
    ) 
    user = result.scalar_one_or_none()

    if not user :
        raise HTTPException(
            status_code= 404 , 
            detail="information is not found"
        )
    
    # update user 

    user.name = payload.name
    
    await db.commit()
    await db.refresh(user)

    return user


# to remove the element and rowss 

@app.delete("/db/users/{user_id}")
async def delete_element_in_database(user_id :int , 
                                     db : AsyncSession = Depends(get_db)) :
    result = await db.execute(
        select(UserModel).where(UserModel.id == user_id)
    )

    deletedata = result.scalar_one_or_none()

    if not deletedata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND , 
            detail="user is not found"
        )
    
    await db.delete(deletedata)  # this is how you can delete the data okay 
    await db.commit()

    return {
        "messages" : "selected user is delete sucessfully"
    }



# ==============================================================================
# 3. PRODUCTS OPERATIONS (TOP 10 & CATALOG)
# ==============================================================================
@app.get("/db/products/top-10", response_model=List[ProductResponse], tags=["Products (PostgreSQL)"])
async def get_top_10_products(db: AsyncSession = Depends(get_db)):
    """Fetches TOP 10 highest-priced products from 'products' table."""
    query = select(ProductModel).order_by(ProductModel.price.desc()).limit(10)
    result = await db.execute(query)
    return result.scalars().all()

  
@app.get("/db/products", response_model=List[ProductResponse], tags=["Products (PostgreSQL)"])
async def get_products(
    category: Optional[str] = Query(None, description="  filter (e.g. Books, Electronics)"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Fetches products with optional category filter."""
    query = select(ProductModel)
    if category:
        query = query.where(func.lower(ProductModel.category) == category.lower())
    query = query.order_by(ProductModel.id.asc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()  

# ==============================================================================
# EXISTING BASIC LEARNING EXAMPLES
# ==============================================================================
class studentdetail(BaseModel):
    name: str
    rollno: int


@app.get("/information", tags=["Basic Examples"])
def get_information():
    return {"message": "Data is being fetched. Please wait..."}


@app.post("/postdata", tags=["Basic Examples"])
def postinformation(details: studentdetail):
    return {"message": f"user successfully created account with name {details.name}"}


