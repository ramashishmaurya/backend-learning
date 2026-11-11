
# def recursionprinting(n:int) :

#     if (n == 1 ) :
#         return 1 
    
#     else:
#         print(recursionprinting(n-1))
    
# recursionprinting(5)


# def fibonacci(n:int) ->int :

#     if n <=1:
#         return n 
    
#     else:
#         return fibonacci(n-1) + fibonacci(n-2)

# print(fibonacci(4))

# numbers = [1 , 2 , 4 , 5 , 4 ]

# # this is goal to return that number first index okay 
# keys = 6
# for i in range(len(numbers)) :

#     if keys not in numbers : # this line of code check the keys not present return  to the not available okay 
#         print("keys is not present in the list")
#         break
#     if i == len(numbers) :
#         print(-1)

#     if numbers[i] == keys :

#         print(i)
#         break


# name = "ashish is here "

# result = []
# listname = name.split()

# for  i in range(len(listname)) :

#     b = listname[i][0].upper() + listname[i][1:] ->> give me start from 1 add to next string okay 
#     result.append(b)  

# abc = " ".join(result)
# print(abc)


# n = 4

# def tilingmanagement(n : int) -> int :

#     if n == 1 or n == 0 :
#         return 1 
    
#     return tilingmanagement(n-1) + tilingmanagement(n-2)

# print(tilingmanagement(n))


# second hights mummbe 


# number = [1 , 5 , 6 , 8 , 9 , 10 ]

# def secondhighestnumber(number) :

#     max_number = max(number)

#     second_highest = 0 

#     for i in number :

#         if i < max_number and i > second_highest :

#             second_highest = i 

#     return second_highest

# print(secondhighestnumber(number))


# name = "Apnacollage".strip().lower()

# def duplicatedstring(name) :

#     character = ""

#     for i in name :

#         if i not in character :

#             character += i   # checking of valeus not present do this okay  right 
        
#     return character

# print(duplicatedstring(name))


# remove d uplicated 

# def removeduplicated(name) :

#     sets = set()
#     result = []

#     for  i in name :
#         if i  not in sets :  # need to underatsna how i can do this program as well oaky 
#             result.append(i)
#             sets.add(i)
        
#     return "".join(result)


# print(removeduplicated("Banana"))

# def partcouplepair(n : int) -> int :

#     if (n==1 or n == 2 ) :  # if there is two people has to 2 ways okay 

#         return n 

#     else:

#         return partcouplepair(n-1) +(n-1) * partcouplepair(n-2)
    

# print(partcouplepair(2))


# def functiongetdata():
#     return "getting data from function as followed righ  okay"


# from fastapi import BackgroundTasks , FastAPI 


# def functiontaskadd( backgroundtask : BackgroundTasks):

#     backgroundtask.add_task(functiongetdata) 


# def numberadd(x) :

#     return x + 2 

# def test_answer():
#     assert numberadd(3) == 5 


# test_answer()

# as rih make sens eas righ as planned right  as planned right laky


# print string builder 

# def printstringbuilder(n:int , lastplacee : int ) :

#     stringbuilder = ""

#     if (lastplacee == 0):
#         stringbuilder += "0"
 
def generator(n , s ) :  # here n -->> defined n defined the lenght of string 

    if len(s) ==n :
        print(s)
        return   
    
    generator(n , s + "0")  #  this is itself called bhai okay right 

    if len(s) == 0 or s[-1] == "0" :

        generator(n , s + "1")

 
n = 3 

generator(n , "")

print(generator(0 , ""))


