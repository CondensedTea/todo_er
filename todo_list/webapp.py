from flask import Blueprint, current_app, redirect, render_template, request, url_for

TASKS_PER_PAGE = 5

todo_list_app = Blueprint('todo_list_app', __name__, template_folder='templates')


@todo_list_app.route('/')
def root():
    return redirect(url_for('todo_list_app.tasks')), 302


@todo_list_app.route('/tasks')
def tasks():
    page = request.args.get('p', type=int, default=1)
    state = request.args.get('state', type=str, default='new')
    db = current_app.config['DATABASE']
    if state == 'all':
        tasklist, next_page_flag = db.get_tasklist_all(page)
    else:
        tasklist, next_page_flag = db.get_tasklist_specific(state, page)
    return (
        render_template(
            'mixed_tasks_list_template.html',
            tasklist=tasklist,
            page=page,
            current_state=state,
            tpp=TASKS_PER_PAGE,
            is_there_next_page=next_page_flag,
        ),
        200,
    )


@todo_list_app.route('/complete')
def complete_task_handle():
    task_id = request.args.get('task', type=int)
    db = current_app.config['DATABASE']
    db.complete_task(task_id)
    return redirect(url_for('todo_list_app.tasks', p=1, state='new')), 200


@todo_list_app.route('/add_task')
def add_task_handle():
    description = request.args.get('desc', type=str)
    db = current_app.config['DATABASE']
    db.add_task(description)
    return redirect(url_for('todo_list_app.tasks', p=1, state='new')), 201


@todo_list_app.route('/search')
def search_task_handler():
    page = request.args.get('p', type=int, default=1)
    query = request.args.get('query', type=str)
    db = current_app.config['DATABASE']
    tasklist, next_page_flag = db.get_tasklist_all(page, search_string=query)
    return (
        render_template(
            'arrows_for_search_template.html',
            tasklist=tasklist,
            page=page,
            current_page='todo_list_app.search_task_handler',
            tpp=TASKS_PER_PAGE,
            search_string=query,
            is_there_next_page=next_page_flag,
        ),
        201,
    )
