
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
origins = [
    "http://localhost:3000", 
    "https://www.meriwebsite.com",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)


class student(BaseModel):
    name : str 
    graduation : str 

@app.get("/")
def rootdata():
    return "data is able to fetched right"


@app.post("/api/getdata/")
def postgetdata(b:student):
    return {
        "studentsata " : b 
    }

@app.post("/data/{items_id}/")
def postdata(items_id : int ):
    return {
        "returnnumber " : items_id
    }
 
