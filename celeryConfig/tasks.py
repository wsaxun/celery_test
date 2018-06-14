from celery.signals import task_failure, task_success
from .app import app


@app.task(bind=True)
def test(self):
    print(dir(self))
    print('test')
    return 'test'


@app.task
def add(x, y):
    print('add')
    return x + y


@task_failure.connect
def task_fail_handler(*args, **kwargs):
    print(args)
    print(kwargs)


@task_success.connect
def task_success_handler(*args, **kwargs):
    print('xums')
    print(args)
    print(kwargs)
