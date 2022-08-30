from flask.cli import load_dotenv
from api import create_app
from api.extensions import celery as cry


load_dotenv()
app = create_app()
celery = cry.init_app(app)
