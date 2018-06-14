import json
from django.http import JsonResponse
from celeryConfig import tasks
from django.core import serializers
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django_celery_results.models import TaskResult



# Create your views here.


def add(request):
    x = request.GET.get('x')
    y = request.GET.get('y')
    task = tasks.add.delay(x, y)
    return JsonResponse([task.id], safe=False)


def test(request):
    task = tasks.test.delay()
    return JsonResponse([task.id], safe=False)


def add_task(request):
    schedule, created = IntervalSchedule.objects.get_or_create(every=10,
                                                               period=IntervalSchedule.SECONDS, )
    PeriodicTask.objects.create(
        interval=schedule,  # we created this above.
        name='test-beat3',  # simply describes this periodic task.
        task='celeryConfig.tasks.test',  # name of task.
    )
    return JsonResponse([1], safe=False)


def query(request):
    task_id = request.GET.get('id')
    r = serializers.serialize('json', TaskResult.objects.filter(task_id=task_id))
    r = json.loads(r)
    return JsonResponse(r, safe=False)
