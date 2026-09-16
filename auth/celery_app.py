from celery import Celery

redis_url = "redis://localhost:6379/0"

celery_app = Celery(
    "background_worker" , 
    broker=redis_url , 
    backend=redis_url,
    include=["tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    timezone="Asia/Kolkata",
)

