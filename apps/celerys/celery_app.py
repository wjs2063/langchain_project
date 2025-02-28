"""
Run celery worker

poetry run celery --app=apps.celerys.celery_app.app worker --concurrency=1 --loglevel=DEBUG
"""

import os

from celery.app import Celery

redis_url = os.getenv("REDIS_URL", "redis://localhost:6378")
postgres_url = "db+postgresql://postgres:postgres@localhost:8080/postgres"

app = Celery(
    name="task",
    broker=redis_url,
    backend=postgres_url,
)
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
)


@app.task
def celery_add(x: int, y: int) -> int:
    z = x**2 + y**2
    return {"result": z}


from typing import List

from apps.utils.smtp.send_email import send_email


@app.task
def celery_send_email(to_email: List[str], subject: str, body: str):
    send_email(to_email=["wjs2063@naver.com"], subject="hi", body="hello")
