import json
from django.http import JsonResponse
from celeryConfig import tasks
from django.core import serializers
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, \
    PeriodicTask
from django_celery_results.models import TaskResult
from celery.result import AsyncResult


# Create your views here.


def get_or_create_interval(interval_type='SECONDS', interval=10):
    if interval_type == 'SECONDS':
        result = IntervalSchedule.objects.get_or_create(every=interval,
                                                        period=IntervalSchedule.SECONDS)
    elif interval_type == 'DAYS':
        result = IntervalSchedule.objects.get_or_create(every=interval,
                                                        period=IntervalSchedule.DAYS)
    elif interval_type == 'HOURS':
        result = IntervalSchedule.objects.get_or_create(every=interval,
                                                        period=IntervalSchedule.HOURS)
    elif interval_type == 'MINUTES':
        result = IntervalSchedule.objects.get_or_create(every=interval,
                                                        period=IntervalSchedule.MINUTES)
    elif interval_type == 'MICROSECONDS':
        result = IntervalSchedule.objects.get_or_create(every=interval,
                                                        period=IntervalSchedule.MICROSECONDS)
    else:
        raise Exception('interval type error')
    return result


def get_or_create_crontab(crontab): # '*/4 * * * *'
    crontab = crontab.strip()
    crontabs = crontab.split()
    result = CrontabSchedule.objects.get_or_create(minute=crontabs[0],
                                                   hour=crontabs[1],
                                                   day_of_week=crontabs[2],
                                                   day_of_month=crontabs[3],
                                                   month_of_year=crontabs[4])
    return result


def create_task(schedule, name, task, *args, **kwargs):
    if isinstance(schedule[0], IntervalSchedule):
        if args and kwargs:
            PeriodicTask.objects.create(
                interval=schedule[0],
                name=name,
                task=task,
                args=json.dumps(args),
                kwarg=json.dumps(kwargs)
            )
        elif args:
            PeriodicTask.objects.create(
                interval=schedule[0],
                name=name,
                task=task,
                args=json.dumps(args)
            )
        elif kwargs:
            PeriodicTask.objects.create(
                interval=schedule[0],
                name=name,
                task=task,
                kwarg=json.dumps(kwargs)
            )
        else:
            PeriodicTask.objects.create(
                interval=schedule[0],
                name=name,
                task=task,
            )
    elif isinstance(schedule[0], CrontabSchedule):
        if args and kwargs:
            PeriodicTask.objects.create(
                crontab=schedule[0],
                name=name,
                task=task,
                args=json.dumps(args),
                kwarg=json.dumps(kwargs)
            )
        elif args:
            PeriodicTask.objects.create(
                crontab=schedule[0],
                name=name,
                task=task,
                args=json.dumps(args)
            )
        elif kwargs:
            PeriodicTask.objects.create(
                crontab=schedule[0],
                name=name,
                task=task,
                kwarg=json.dumps(kwargs)
            )
        else:
            PeriodicTask.objects.create(
                crontab=schedule[0],
                name=name,
                task=task
            )


def add(request):
    x = request.GET.get('x')
    y = request.GET.get('y')
    task = tasks.add.delay(x, y)
    return JsonResponse([task.id], safe=False)


def test(request):
    task = tasks.test.delay()
    return JsonResponse([task.id], safe=False)


def add_task(request):
    # schedule = get_or_create_interval(interval_type='SECONDS', interval=120)
    schedule = get_or_create_crontab('*/3 * * * *')
    create_task(schedule, 'test-beat2', 'celeryConfig.tasks.add', 12, 12)
    return JsonResponse([1], safe=False)


def delete_task(request):
    name = request.GET.get('name')
    PeriodicTask.objects.filter(name=name).delete()
    return JsonResponse([], safe=False)


def change_task(request):
    name = request.GET.get('name')
    # task = PeriodicTask.objects.get(name=name)
    task = PeriodicTask.objects.filter(name=name)
    if task.enabled:
        task.enabled = False
    else:
        task.enabled = True
    task.save()
    return JsonResponse([], safe=False)


def query_task(request):
    name = request.GET.get('task_name')
    if not name:
        r = list(PeriodicTask.objects.all())
        result = []
        for i in r:
            result.append(
                {'name': i.name, 'enabled': i.enabled, 'task': i.task,
                 })
    else:
        r = serializers.serialize('json',
                                  PeriodicTask.objects.filter(name=name))
        result = json.loads(r)
    return JsonResponse(result, safe=False)


def query(request):
    task_id = request.GET.get('id')
    r = serializers.serialize('json',
                              TaskResult.objects.filter(task_id=task_id))
    r = json.loads(r)

    return JsonResponse(r, safe=False)
