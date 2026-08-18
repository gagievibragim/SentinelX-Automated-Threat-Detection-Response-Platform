from app.worker.celery_app import celery_app

@celery_app.task
def process_background_event(event_id: int):
    return {"event_id": event_id, "status": "processed"}
