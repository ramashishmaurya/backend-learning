import select
from fastapi import FastAPI, Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , func
from auth import get_db 
from auth import User , Responsemodel
from auth import CreateUser , LoginRequest , Updateinformation
from jose import jwt 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta, timezone

from auth import Project , Employee , Department , Sales , Orders
app = FastAPI()

@app.get("/getdata")
async def fetchedinformation(db :AsyncSession = Depends(get_db)):

    stmt = select(
        Orders.order_status , 
        func.count(Orders.order_id).label("total_orders")
    ).group_by(Orders.order_status)

    result = await db.execute(stmt)

    b = result.mappings().all()

    return b

