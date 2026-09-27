# import time

# from celery_app import celery


# @celery.task
# def send_email(email: str, message: str):

#     print("Email task started")

#     time.sleep(5)

#     print(f"Sending email to {email}")
#     print(f"Message: {message}")

#     return "Email sent successfully"



n = "Programming"

def functiocountstring(n):

    result = {}

    for i in n :

        if i not in result:
            result[i] = 1 
        else:
            result[i] += 1 
    return result

abc = functiocountstring(n)
print(abc)


