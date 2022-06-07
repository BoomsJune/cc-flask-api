from api.extensions.celery import celery


@celery.task(time_limit=60)
def index():
    return "ok"
