class CeleryConfig(object):
    broker_url = 'redis://172.17.0.3:6379/0'
    timezone = 'UTC'
    # result_backend = 'redis://172.17.0.3:6379/1'
    result_backend = 'django-db'
    result_expires = 60 * 60 * 24 * 60
    result_serializer = 'json'
    result_persistent = True
    accept_content = ['json', 'msgpack']
    task_track_started = True
    imports = ['celeryConfig.tasks']
    beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
