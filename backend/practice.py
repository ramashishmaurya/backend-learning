
# this is probelms that  we need to work okay 

# print all the number okay has only th if the number is 1 conservative okay 


# def binarystring(n :int , chars : str) :


#     if len(chars) == n :
#         print(chars)

#         return chars

#     binarystring(n , chars+"0")

#     if len(chars) == 0 or chars[-1] == "0" :

#         binarystring(n  , chars + "1")


# print(binarystring(3 , ""))


# arrays = [3, 2, 4, 5, 6, 2, 7, 2, 2]
# keys = 2 

# def searchindexnumber(arrays, keys, index=0):

#     # Base case .....   
#     if index == len(arrays): 
#         return []

#     # Recursive call
#     result = searchindexnumber(arrays, keys, index + 1)  

#     # Check current element
#     if arrays[index] == keys:
#         return [index] + result   

#     return result


# print(searchindexnumber(arrays, keys))



# def numbertostringpresentation(n):
#     words = {
#         0: "zero", 1: "one", 2: "two",
#         3: "three", 4: "four", 5: "five",
#         6: "six", 7: "seven", 8: "eight",
#         9: "nine"
#     }  

#     if n == 0:
#         return ""

#     return numbertostringpresentation(n // 10) + words[n % 10] + " "  # thisnis last one track the values 


# inputs = 1234

# output = numbertostringpresentation(inputs).strip()
# print(output)

# from fastapi import FastAPI , Depends


# app = FastAPI(title="basic fastapi routes" )

# def get_name():
#     return "Ashish maurya"

# @app.get("/getdata")
# def get_information(name :str = Depends(get_name)) :   

#     return name  


# def pagingproblem(page: int = 10  , skip : int = 10) :

#     return {
#         "pages" : page , 
#         "skipvalues" : skip
#     }

# @app.get("/products")
# def productdetails(paging :dict = Depends(pagingproblem , use_cache=False)): # one you call the depends then caches this olkay righ 
#      return {
#          'messages' : 'product is fetched' ,   
#          "data" : paging
#     }


# from fastapi.middleware.cors import CORSMiddleware

# # backgrounds task 


# from fastapi import FastAPI, BackgroundTasks

# app = FastAPI()

# def send_email(email: str):
#     print(f"Sending email to {email}")
#     print("Welcome email sent!")


# @app.post("/register")
# async def register(
#     email: str,
#     background_tasks: BackgroundTasks
# ):
#     # Add task to execute after response
#     background_tasks.add_task(send_email, email)  # this is exactly we ge the message but that work is doing behind

#     return {
#         "message": "Registration successful",
#         "email": email
#     }



# program to find length of strings using the recursive 

def lengthofstringusingrecur(n, index=0):

    if index == len(n):
        return index

    return lengthofstringusingrecur(n, index + 1) 


print(lengthofstringusingrecur("Ashish"))