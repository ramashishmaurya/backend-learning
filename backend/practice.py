
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


arrays = [3, 2, 4, 5, 6, 2, 7, 2, 2]
keys = 2

def searchindexnumber(arrays, keys, index=0):

    # Base case
    if index == len(arrays):
        return []

    # Recursive call
    result = searchindexnumber(arrays, keys, index + 1)

    # Check current element
    if arrays[index] == keys:
        return [index] + result

    return result


print(searchindexnumber(arrays, keys))
