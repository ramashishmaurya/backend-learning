numbers = [1, 2, 3, 4, 5]

doubled = list(map(lambda x : x**2, numbers)) # here we need to map right okay 


def splitnamecharater(name):
    return name

mapfunction = list(map(splitnamecharater , "ashish"))


users = [
    {"name": "Aman", "email": "aman@gmail.com"},
    {"name": "Neha", "email": "neha@yahoo.com"},
    {"name": "Ravi", "email": "ravi@hotmail.com"}
]

get_email = lambda user : user['email']

dt = list(map(get_email , users))

print(dt)


from fastapi import FastAPI


app = FastAPI()

@app.get("/datas")
def information():
    return({
        "datainfomation" : "getting the datainfomation"
    })


from pydantic import BaseModel , EmailStr

class Groupsdata(BaseModel):
    username : str 
    emails : EmailStr

class Items(BaseModel):
    description: str | None = None
    price : float 


listn = ["acb" , "abc" , "cde" , "dec"]

def Groupsanagrama(listn): 
    result = {}

    for i in  listn:
        key = ''.join(sorted(i))

        if key not in result:

            result[key] = []  
        
        result[key].append(i)
    return(list(result.values()))



