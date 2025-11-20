from celery import Celery

app = Celery("test")
app.autodiscover_tasks()
