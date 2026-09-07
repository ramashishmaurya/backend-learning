import select
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from auth import get_db
from auth import User
from auth import CreateUser

app = FastAPI()

@app.post("/users/")
async def create_user(
    user : CreateUser , 
    db : AsyncSession = Depends(get_db)
):
    new_user = User(
        name = user.name , 
        email = user.email , 
        password = user.password

    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    
    }


@app.get("/getdata/")
async def get_information(db : AsyncSession = Depends(get_db)
):
    result = await db.execute(
    select(User)
)
    user = result.scalars().all()

    return{
        "data" : user
    }
    

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


