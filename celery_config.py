# celery_config.py
from celery import Celery

def make_celery(app_name=__name__):
    return Celery(
        app_name,
        broker='amqp://user:password@localhost:5672',
        broker_connection_retry_on_startup=True,
        backend='redis://localhost:6379/0'
    )

celery = make_celery()
