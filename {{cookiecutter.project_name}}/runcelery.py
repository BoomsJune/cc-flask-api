from flask.cli import load_dotenv
from api import create_app
from api.extensions import celery


load_dotenv()
app = create_app()
celery = celery.init_app(app)
