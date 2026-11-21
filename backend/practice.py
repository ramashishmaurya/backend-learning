
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

# def lengthofstringusingrecur(n, index=0):

#     if index == len(n):
#         return index  

#     return lengthofstringusingrecur(n, index + 1) 

# print(lengthofstringusingrecur("Ashish"))  

# how i have to focused as  make sense ashow i can do as righ as maek sesense ahow i can do as right as make sense ashow ic an do  as righ make sense how 



# def countSubstrings(S, i=0, j=0):  # "abca"   "" --  return 0 

#     if i == len(S):
#         return 0

#     if j == len(S):
#         return countSubstrings(S, i + 1, i + 1) 

#     count = 0

#     if S[i] == S[j]:  
#         count = 1

#     return count + countSubstrings(S, i, j + 1)


# S = "abcab"
# print(countSubstrings(S))


# second maximum number 


# this is check the second number check max number anc checks two condition each steps okay 
# number = [1 , 3 , 5 , 6 , 7 ]

# def secondhighest(number) :

#     max_number = max(number)
#     second_number = 0 

#     for i in number :

#         if max_number > i and   i > second_number :

#             second_number = i 

#     return second_number

# print(secondhighest(number))


# listname = [1 , 9 , 10 , 5, 6 , 7]

# def bubblesort(listname) :

#     for i in range(len(listname)) :

#         for j in range(len(listname)-i - 1) :

#             if listname[j] > listname[j+1] :

#                 listname[j] , listname[j+1] = nlistname[j+1] , listname[j]
#     return listname

# print(bubblesort(listname))  


# arr = [5, 3, 8, 1, 2]

# for i in range(1, len(arr)):
#     key = arr[i]
#     j = i - 1

#     while j >= 0 and arr[j] > key:
#         arr[j + 1] = arr[j]
#         j = j - 1

#     arr[j + 1] = key

# print("Sorted array:", arr)

# this is j = -1 righ now okay hence right hence  worked  bhai 


def merge_sort(arr) :

    # base condition 

    if len(arr) <= 1 :
        return arr

    # divide arrays into 2 part 

    midpoint = len(arr) // 2   

    left = arr[:midpoint]
    right = arr[midpoint : ]

    # sort both parts 
    left = merge_sort(left) # make the left untill the left becomes the into single okay 
    right = merge_sort(right)

    # merged both sorted part 

    return merge(left , right)

def merge(left, right):

    result = []

    i = 0
    j = 0

    # Compare elements from both lists
    while i < len(left) and j < len(right):

        if left[i] < right[j]:
            result.append(left[i])
            i += 1

        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result


arr = [38, 12, 27, 43, 9, 31, 18, 25]

print("Original Array:", arr)

sorted_arr = merge_sort(arr)

print("Sorted Array:", sorted_arr)

