import sqlite3
from pathlib import Path

import pytest

from todo_list import create_app


@pytest.fixture(name='tasks')
def fixture_tasks():
    return [
        (u'Купить еду в магазине', 'new'),
        (u'Забрать посылку на почте', 'new'),
        (u'Приготовить еду', 'done'),
        (u'Встретится с друзьями', 'done'),
        (u'Прочитать статью', 'done'),
        (u'Поиграть в шахматы', 'new'),
    ]


@pytest.fixture(autouse=True, name='tmp_database')
def fixture_tmp_database(tmp_path, tasks):
    db_path = str(tmp_path / 'tmp_todo_list.sqlite3')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('create table tasklist (description text, status integer)')
    c.executemany('insert into tasklist values (?, ?)', tasks)
    conn.commit()
    yield db_path
    conn.close()
    Path(db_path).unlink()


@pytest.fixture()
def client(tmp_database):
    app = create_app(tmp_database)
    with app.app_context():
        with app.test_client():
            return app.test_client()
