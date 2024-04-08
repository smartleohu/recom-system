import os

from celery import Celery

from recom_system.settings import APP_NAME

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recom_system.settings')

app = Celery(APP_NAME)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Set CELERYD_POOL_RESTARTS to True
app.conf.CELERYD_POOL_RESTARTS = True
