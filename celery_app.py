from celery import Celery

celery = Celery(
    "myapp",
    broker="redis://localhost:6379/0"
)