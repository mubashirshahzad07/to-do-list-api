from flask import Flask

from .api.auth import auth
from .api.todo import todo


def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth)
    app.register_blueprint(todo)

    app.json.sort_keys = False

    return app