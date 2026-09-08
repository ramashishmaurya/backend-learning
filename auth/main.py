import select
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from auth import get_db 
from auth import User , Responsemodel
from auth import CreateUser
from jose import jwt 

from datetime import datetime, timedelta, timezone

from auth import hash_password , verify_password

app = FastAPI()

@app.post("/users/")
async def create_user(
    user : CreateUser , 
    db : AsyncSession = Depends(get_db)
):
    new_user = User(
        name = user.name , 
        email = user.email , 
        password = hash_password(user.password)

    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    
    }

SECRET_KEYS = "8zxHBOkiYT5roos1I6hKs1qxluBT9Z7JzG8DfUXrpVU"
ALGORITHM = "HS256"
EXCESS_EXPIRY_MINUTES = 30 

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({'exp' : expire})

    encode_jwt = jwt.encode(to_encode , SECRET_KEYS , algorithm=ALGORITHM)

    return encode_jwt



@app.get("/getdata/", response_model=list[Responsemodel])  
async def get_information(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User)
    )

    user = result.scalars().all()

    return user
    

@app.get("/pdata/{id}/")
async def getdata(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        return {
            "message": "User not found"
        }

    return {
        "datainformation": user
    }


@app.delete("/userdelete/{id_name}/")
async def userdeleteinformation(id_name:int , db : AsyncSession= Depends(get_db)) :
    result = await db.execute(
        select(User).where(User.id == id_name)
    )

    rs = result.scalar_one_or_none()

    if rs is None:
        return {"messages" : "Product not found"}
    
    await db.delete(rs)
    await db.commit()

    return{"messages" : "product deleted successfully"}


