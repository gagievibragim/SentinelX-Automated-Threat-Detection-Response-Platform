from celery import Celery
from app.config import settings

celery_app = Celery("sentinelx", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]

@celery_app.task
def health_task():
    return {"status": "ok"}
