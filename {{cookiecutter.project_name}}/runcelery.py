from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv() or ".flaskenv")


from api.extensions import celery  # noqa: E402
import api  # noqa: E402

app = api.create_app()
celery = celery.init_app(app)
