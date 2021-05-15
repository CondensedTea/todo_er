import sqlite3
from typing import NamedTuple


class Task(NamedTuple):
    id: int
    value: str
    status: str


class Database:
    def __init__(self, file):
        self.tpp = 5
        self.connection = sqlite3.connect(file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_tasklist_specific(self, state, page):
        tasklist = []
        query = 'select ROWID, * from tasklist where status = ? limit ?, ?'
        params = (state, (page - 1) * self.tpp, self.tpp + 1)
        for row in self.cursor.execute(query, params):
            tasklist.append(Task(row[0], row[1], row[2]))
        if len(tasklist) == self.tpp + 1:
            return tasklist[:-1], True
        return tasklist, False

    def get_tasklist_all(self, page, search_string=None):
        tasklist = []
        query = (
            'select ROWID, * from tasklist limit ?, ?'
            if search_string is None
            else 'select ROWID, * from tasklist where description like ? limit ?, ?'
        )
        params = (
            ((page - 1) * self.tpp, self.tpp + 1)
            if search_string is None
            else (f'%{search_string}%', (page - 1) * self.tpp, self.tpp + 1)
        )
        for row in self.cursor.execute(query, params):
            tasklist.append(Task(row[0], row[1], row[2]))
        if len(tasklist) == self.tpp + 1:
            return tasklist[:-1], True
        return tasklist, False

    def complete_task(self, row_id):
        query = "update tasklist set status = 'done' where ROWID = ?"
        self.cursor.execute(query, (row_id,))
        self.connection.commit()

    def add_task(self, description):
        query = 'insert into tasklist (description, status) values (?, ?)'
        self.cursor.execute(query, (description, 'new'))
        self.connection.commit()
