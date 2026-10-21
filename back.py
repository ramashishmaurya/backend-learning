import time 
import os 

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")   

celery_app = Celery(
    "research_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["worker.tasks"]
)


@celery_app.task
def send_Email_use(user_email : str ) -> str : 

    print(f"starting the email id {user_email}")

    time.sleep(10)

    print(f"Emails has been sent successfully {user_email}")




from fastapi import FastAPI

from back import send_Email_use

app = FastAPI()

app.post("signup/")
def  userr_singup(email_id : str ):
    """there is the email i will get from the  user in the parameter okay """

    send_Email_use.delay(email_id)

    return "Email is created successfully on the terminal bhai okay "



