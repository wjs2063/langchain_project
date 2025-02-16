celery_borker_url = "redis://localhost:6378"
CELERY_RESULT_BACKEND = "db+postgresql://postgres:postgres@localhost:8080/postgres"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"  # `json`으로 변경
# CELERY_ACCEPT_CONTENT = ["json"]  # `json`만 허용
CELERY_ACCEPT_CONTENT = ["application/json"]
