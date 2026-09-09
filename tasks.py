import time

from celery_app import celery


@celery.task
def send_email(email: str, message: str):

    print("Email task started")

    time.sleep(5)

    print(f"Sending email to {email}")
    print(f"Message: {message}")

    return "Email sent successfully"