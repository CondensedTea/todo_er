import pytest


def test_root(client):
    response = client.get('/')
    assert response.status_code == 302


@pytest.mark.parametrize(
    'html_line',
    [
        '<form action="/add_task">',
        '<form action="/search?p=1">',
        '<a href="/tasks?state=new">Новые задачи</a>',
        '<a href="/tasks?state=done">Выполненные задачи</a>',
        '<a href="/tasks?state=all">Все задачи</a>',
    ],
)
def test_generic_ui(client, html_line):
    response = client.get('/tasks?p=1&state=new')
    assert html_line.encode('utf-8') in response.data


@pytest.mark.parametrize('task', ['Купить еду в магазине', 'Приготовить еду'])
def test_tasks_all(client, task):
    responce = client.get('/tasks?p=1&state=all')
    assert task.encode('utf-8') in responce.data


def test_complete_task(client):
    new_task = 'Купить жидкость для мытья'
    complete_task_link = '/complete?task=7'
    client.get('/add_task?desc=' + new_task)
    client.get(complete_task_link)
    new_tasks_response = client.get('/tasks?state=new')
    assert complete_task_link.encode('utf-8') not in new_tasks_response.data


def test_search_task(client):
    new_task = 'Купить жидкость для мытья'
    client.get('/add_task?desc=' + new_task)
    response = client.get('/search?p=1&query=' + new_task)
    assert response.status_code == 201
    assert new_task.encode('utf-8') in response.data
