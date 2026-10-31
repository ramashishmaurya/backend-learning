


# vowels =['a' , 'e' , 'i' , 'o' , 'u']
# strname = "ashishaeiou"
# countvowels = 0  
# for i in strname :

#     if i in vowels:
#         countvowels+=1

# print("vowels count is \n")
# print(countvowels)  

# listdata = [1 , 2, 3, 4 , 5 , 0 , 2 , 0 , 2 , 0 , 0  ]
# # thsi task is to mpush data in et the end bhai right 

# def pushsdataend(data) :
#     result = []

#     for i in data :

#         if i !=0 :
#             result.append(i)
    
#     for j in data:
#         if j == 0 :
#             result.append(j)

#     return result

# print(pushsdataend(listdata))



# information = [1 , 3 , 4 , 5]

# information.extend([6 , 9])

# print(information)

# information.insert(3 , 100)

# print(information)

# information.remove(100)   

# print(information)


data = [5 , 4 , 2 - 4   , 8 , 1 ]

# insertatio methods used to solve this problens okay 


# def insertionmethod(data) :

#     for i in range(1 , len(data)):

#         currect_data = data[i]

#         j = i - 1 

#         while( j >=0 and  data[j] > currect_data):     

#             data[j+1] = data[j]

#             j = j - 1    
        
#         data[j+1] = currect_data
#     return data

# print(insertionmethod(data))  # rhis selectuion proces  how this could messure tigth bow hwat i cn dioi as planne right okay 




# maxumun profist questuion how you can calculated bhai 


data = [1 , 0 , 4 , 7 , 8 , 3 ] 

# as right as make sens a srigth okay how i can do as right -planned rigth okay how i can do 

# listnumer = [3 , 4 , 6 , 7 , 1 ]


# def bubblesortalgorith(number) :

#     for i in range( len(number) -1 ):

#         for j in range(len(number) - i- 1):

#             if number[j] > number[j+1] :

#                 number[j] , number[j+1] = number[j+1] , number[j]

#     return number


# print(bubblesortalgorith(listnumer))

# name = "Ashish"

# name[0] = "D"
# print(name)  # pythin build this so crucial infomation does not changed bhai okay 



# lets make first works uppercase bhai lets make sense as right okay 


# username = "ashish is about to come"

# words = username.split()

# result = [] # result as follwed bhai 
 
# for word in words :

#     result.append(word[0].upper() + word[1:])  

# final_result = " ".join(result)

# print(final_result)


# data = [12, 45, 7, 89, 34, 89, 23, 56]

# def secondhighestnumber(data) :

#     highestvalues = max(data)

#     secondhighest = float('-inf') 

#     for i in data :

#         if i < highestvalues and  i> secondhighest :

#             secondhighest = i 
        
#     return secondhighest


# print(secondhighestnumber(data))


# checj all zeroes okay 


# data = [0, 5, 0, 3, 8, 0, 2, 9]

# def Zeroattheend(data) :

#     result = []
#     for i in data : 

#         if i != 0 :
#             result.append(i)
        
#     for j in data : 
#         if j == 0 :

#             result.append(j)
    
#     return result


# print(Zeroattheend(data))


# i need to find the missing number 

# data = [1, 2, 3, 5, 6, 7, 8]


# def findmissingnumber(data) :

#     pointerhelpwer = data[0]

#     for i in data :

#         if i == pointerhelpwer :

#             pointerhelpwer+= 1 
#         else:
#             print("this is missing number correct" , pointerhelpwer)   
#             break

# findmissingnumber(data)

data = "aabbcddex"


def non_repeting_values(data) :

    for i in data :  # has s will be i = i 
        count = 0 

        for j  in data :  


            if i == j :

                count+=1

        if count == 1  :  # that valeus presend only once okay  maea of count is 1 - retun ths ola 
           return i
        
    return None

print(non_repeting_values(data))

