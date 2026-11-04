
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


name = "Apnacollage".strip().lower()

def duplicatedstring(name) :

    character = ""

    for i in name :

        if i not in character :

            character += i   # checking of valeus not present do this okay  right 
        
    return character

print(duplicatedstring(name))