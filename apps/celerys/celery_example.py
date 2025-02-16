from apps.celerys.celery_app import celery_add

result = celery_add.delay(3, 5)
print(result.status)
print(result.get())
