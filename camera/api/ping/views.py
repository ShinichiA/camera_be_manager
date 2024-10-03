from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from camera.celery_tasks.background_tasks.tasks import long_running_task
from camera.core.permissions import IsSuperuserUser


@api_view(['GET'])
@permission_classes([IsSuperuserUser])
def ping(request):
    long_running_task.delay("param")
    return HttpResponse("pong")
