import json

database = {
    "name" : "Ashish maurya" , 
    "subject" : "Hindi"
}

print(type(database))


finalresult = json.dumps(database)

print(finalresult)

# here is we dumped data into the str json formate serialization works
