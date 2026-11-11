from fastapi import FastAPI

from pydantic import BaseModel


class studentdetail(BaseModel) :

    name : str 
    rollno : int 


app = FastAPI(
    summary="This is my API"
)

@app.get("/information")
def get_information():
    return {
        "message": "Data is being fetched. Please wait..."
    }


@app.post("/postdata") 
def postinformation(details : studentdetail):

    return{
        f"user is sucessfully created the accound name is {details.name}"
    }


def my_decorator(func):

    def wrapper():
        print("Function start hone wala hai")

        func()

        print("Function complete ho gaya")

    return wrapper


@my_decorator
def say_hello():
    print("Hello Bhai!")


say_hello()



class student :

    def __init__(self , name , maths) :
        self.maths = maths 
        self.name = name

    
student = student("Ashish" , 122)
print(student.name)


from dataclasses import dataclass

@dataclass  
class student : 
    Name : str
    division : int 

std = student("ahsis" , 10)

print(std.division)


 