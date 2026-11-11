
from .recur import partcouplepair 


from fastapi import FastAPI

app = FastAPI(summary="this will database management system works")


@app.get("/information")
def getinformation():
    return {
        "messsages" : "data is being fatched wait ...."
    }