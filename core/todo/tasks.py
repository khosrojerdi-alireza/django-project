from celery import shared_task
from .models import Task


@shared_task
def getCompletedTask():
    task = Task.objects.filter(complete = True)
    print(task)
    if task:
        for t in task:
            t.delete()
    
