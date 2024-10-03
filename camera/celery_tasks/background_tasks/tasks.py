from celery import shared_task
from celery.task import task
import time


@shared_task
def long_running_task(param):
    # Ví dụ về một task dài hạn
    time.sleep(10)
    return f'Task completed with parameter: {param}'
