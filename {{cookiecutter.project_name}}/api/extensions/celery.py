from celery import Celery


celery = Celery()


def init_app(app):
    """初始化celery"""
    celery = Celery(app.import_name, include=["api.tasks"])
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
