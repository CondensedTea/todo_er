from flask import Flask

from todo_list.sqlite_connector import Database
from todo_list.webapp import todo_list_app


def create_app(path='todo_list/todo_list.sqlite3'):
    app = Flask(__name__)
    app.register_blueprint(todo_list_app)
    app.config['DATABASE'] = Database(file=str(path))
    return app
