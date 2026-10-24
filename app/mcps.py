from fastmcp import FastMCP

mcp = FastMCP("My Assistant Tools 🚀")

@mcp.tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    return f"Weather in {city}: 24°C, Sunny"

if __name__ == "__main__":
    # HTTP server start karega port 8000 pe
    mcp.run(transport="http", port=8000)  # runs on streaming 

 
#arrasts = [5 , 3 , 2 , 1]  # byusing the help of index here i will insert here okay bhau right okay bhai right

# for i in range( 1, len(arrasts)) :

#     current_vals = arrasts[i]

#     j = i -1 

#     while j>=0 and arrasts[j] > current_vals :

#         arrasts[j+1] = arrasts[j]

#         j = j -1 

#     arrasts[j+1] = current_vals


# print(arrasts)



# understant this is our problems okay bhai 

# liststring = ["flowers" , "flower" , "flows"]

# chat = ""

# for n in range(len(liststring[0])) : 

#     for i in liststring :   # need the eitwhy this first one has  7 words okay bhai right but compare to all hasve less words okay bhai right 

#         if n == len(i) or  i[n] != liststring[0][n] :
#             print(chat)
#             exit()

#     chat+= liststring[0][n]  


# print(chat)


 
 # selectio sort righ okay 



# numbvers = [5 , 4, 3 , 2 , 1 ]

# def selectionsort(nums) :

#     for i in range(len(nums)-1) :

#         minpoint = i 

#         for j in range(i+1, len(nums))  : 

#             if nums[minpoint] > nums[j] : 

#                 minpoint = j   
        
#         temp = nums[i]

#         nums[i] = nums[minpoint]

#         nums[minpoint] = temp

#     return nums

# print(selectionsort(numbvers))



# inserdsort cpde 

# arrays = [5 , 4 , 3 , 2 ,1]

# def Selectionsortalgorithm(nums) : 

#     for i in range(len(arrays)) : 

#         minpoint = i 

#         for j in range( i + 1 , len(arrays)) :

#             if arrays[minpoint] > arrays[j] :

#                 minpoint = j 
        
#         temp = arrays[i]  # [1 , 2 , 3 , 4 ]

#         arrays[i] = arrays[minpoint]

#         arrays[minpoint] = temp
#     return arrays


# print(Selectionsortalgorithm(arrays))



# count the frequency bhai okay 

# name = "Ashish"

# def countletter(name)  :

#     result = {}

#     for i in name : 

#         if i not in result : 

#             result[i] = 1 
#         else:

#           result[i]+= 1  

#     return result

# print(countletter(name))


# heights = [7, 3, 6, 4, 6, 2]

# def rainwatertrapped(height):
#     rainwatertrapped = 0

#     for n in range(len(height)):
#         left_max = max(height[:n+1])  
#         right_max = max(height[n:])

#         waterlevel = min(left_max, right_max)

#         rainwatertrapped += max(0, waterlevel - height[n])

#     return rainwatertrapped

# print(rainwatertrapped(heights))


# here we are learning the insertion algorith bhai okay 

