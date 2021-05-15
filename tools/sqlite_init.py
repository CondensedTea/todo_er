import sqlite3
from pathlib import Path


def create_db(path=(Path() / 'todo_list' / 'todo_list.sqlite3')):
    tasks = [
        (u'Купить еду в магазине', 'new'),
        (u'Забрать посылку на почте', 'new'),
        (u'Приготовить еду', 'done'),
        (u'Встретится с друзьями', 'done'),
        (u'Прочитать статью', 'done'),
        (u'Поиграть в шахматы', 'new')
    ]
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('create table tasklist (description text, status integer)')
    c.executemany('insert into tasklist values (?, ?)', tasks)
    conn.commit()
    conn.close()
    return path

if __name__ == '__main__':
    create_db()