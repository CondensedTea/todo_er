from typing import NamedTuple

import pytest

from todo_list.sqlite_connector import Database, Task


class TaskPages(NamedTuple):
    page: int
    ids: list


@pytest.mark.parametrize(
    'state,expected',
    [
        (
            'new',
            [
                Task(id=1, value='Купить еду в магазине', status='new'),
                Task(id=2, value='Забрать посылку на почте', status='new'),
                Task(id=6, value='Поиграть в шахматы', status='new'),
            ],
        ),
        (
            'done',
            [
                Task(id=3, value='Приготовить еду', status='done'),
                Task(id=4, value='Встретится с друзьями', status='done'),
                Task(id=5, value='Прочитать статью', status='done'),
            ],
        ),
    ],
)
def test_get_tasklist_specific(tmp_database, state, expected):
    db = Database(file=tmp_database)
    tasklist, _ = db.get_tasklist_specific(page=1, state=state)
    assert tasklist == expected


def test_get_tasklist_all(tmp_database):
    expected = [
        Task(id=1, value='Купить еду в магазине', status='new'),
        Task(id=2, value='Забрать посылку на почте', status='new'),
        Task(id=3, value='Приготовить еду', status='done'),
        Task(id=4, value='Встретится с друзьями', status='done'),
        Task(id=5, value='Прочитать статью', status='done'),
    ]
    db = Database(file=tmp_database)
    tasklist, _ = db.get_tasklist_all(page=1)
    assert tasklist == expected


def test_complete_task(tmp_database):
    db = Database(file=tmp_database)
    db.complete_task(1)
    tasklist, _ = db.get_tasklist_all(page=1)
    assert tasklist[0].status == 'done'


def test_add_task(tmp_database):
    new_task_text = 'Сходить к зубному'
    db = Database(file=tmp_database)
    db.add_task(new_task_text)
    tasklist, _ = db.get_tasklist_specific(page=1, state='new')
    assert tasklist[-1].value == new_task_text
