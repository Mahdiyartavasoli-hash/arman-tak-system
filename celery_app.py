from celery import Celery
import time

celery_app = Celery(
    "arman_tak_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def generate_heavy_analytics_report(machine_id: int):   
    time.sleep(5)
    return {
        "status": "completed",
        "machine_id": machine_id,
        "summary": f"Heavy production analytics generated for machine #{machine_id}"
    }