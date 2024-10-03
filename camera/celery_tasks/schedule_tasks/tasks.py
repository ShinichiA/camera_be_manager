import time
from contextlib import contextmanager
from datetime import timedelta, datetime

from celery import shared_task, task
from django.core.cache import cache


@shared_task
def check_online():
    """
        schedule: every 5 minutes
        description: check online
    """
    return "Check online"
