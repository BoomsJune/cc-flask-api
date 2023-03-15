import sys
import os

from flask.cli import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.insert(0, BASE_DIR)


from api import create_app


"""测试下脚本
"""


def get_data():
    import requests
    from api.exception import RequestAPIError

    res = requests.get("http://localhost:5000/api/auth/user_list")
    if res.status_code != 200:
        raise RequestAPIError(res)
    print(res.text)


if __name__ == "__main__":

    app = create_app()
    with app.app_context():
        get_data()
