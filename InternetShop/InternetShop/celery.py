import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InternetShop.settings")

app = Celery("InternetShop")
app.config_from_object("django_conf:settings", namespace="CELERY")
app.autodiscover_tasks()
