from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv() or ".flaskenv")


import api  # noqa: E402


app = api.create_app()
