# def function(func):

#     def dealwithperson(fuck):
#         def wrapper():
#             print("hellp=o ji ")
#             func()
#             print("bye ji")
#             fuck()
#         return wrapper
#     return dealwithperson


# def func():
#     print("this is func function right")

# @function(func)
# def fuck():
#     print('function of fuck')

# fuck()


# def arguments(*args):
#     print(args)

# arguments(12,12,4)

from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession
from fastapi import FastAPI , Depends
from auth import Department , get_db

app = FastAPI()

from sqlalchemy import select
from pydantic import BaseModel 
class abc(BaseModel):
    name : str 

@app.post("/getdata")
def getinformation(state : abc):
    return({
        "datainfomation" : state.name
    })


@app.get("/dbdata")
async def getinfomationdb(db : AsyncSession = Depends(get_db)):
    
    result  = await db.execute(
        select(Department)
    )

    rs = result.scalars().all()

    return rs 

@app.get("/getid/{id_name}")
def dyanmicname(id_name : int):
    return ({
        "idnumbwe" : id_name
    })



from fastapi import APIRouter

post_routes = APIRouter(
    prefix="/{user_id}/posts"
)

@post_routes.get("/")
def postinformation(user_id : int):
    return({
        "user_id" : user_id , 
        "posts" : []
    })

app.include_router(post_routes)


