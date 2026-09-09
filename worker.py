from fastapi import BackgroundTasks, FastAPI
import time

app = FastAPI()

from auth import Backgroundswork

def send_email(email: str, message: str):
    print("Background task started")

    time.sleep(5)

    print(f"Sending email: {message}")
    print(f"Sending to: {email}")


@app.post("/signup")
def backgroundwork(
    user: Backgroundswork,
    bg_task: BackgroundTasks
):
    print(f"Saving data for: {user.email}")

    bg_task.add_task(
        send_email,
        user.email,
        "Interview is scheduled on Monday"
    )

    return {
        "message": "Account created successfully"
    }

