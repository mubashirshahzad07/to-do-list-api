from flask import Flask

from api.auth import auth
from api.todo import todo


app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(todo)

