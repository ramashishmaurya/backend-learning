from pydantic import BaseModel  , StrictInt

class CharRequest(BaseModel):
    user_id :StrictInt
    query : str

class CharResponse(BaseModel):
    status : str
    response : str 



