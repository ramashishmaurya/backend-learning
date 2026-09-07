from fastapi import FastAPI
from schemas import CharRequest

from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()


@app.post("/api/chat/")
def charrequestdata(state : CharRequest) :
    return{
        "user_id" : state.user_id , 
        "question" : state.query
    }

