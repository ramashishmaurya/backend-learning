from pydantic import BaseModel , EmailStr

class CreateUser(BaseModel):
    name : str 
    email : EmailStr
    password : str


class Responsemodel(BaseModel):
    id : int 
    name : str 
    email : EmailStr

