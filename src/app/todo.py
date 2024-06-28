from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.model import get_db

bp = Blueprint('todo', __name__)


@bp.route('/')
def index():
    db = get_db()
    todos = db.execute(
        'SELECT t.id, content, created, author_id, username'
        ' FROM todo t JOIN user u ON t.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('todo/index.html', todos=todos)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        content = request.form['content']
        error = None

        if not content:
            error = 'content is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO todo (content, author_id)'
                ' VALUES (?, ?)',
                (content, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html') # getならこっち


def get_todo(id, check_author=True):
    todo = get_db().execute(
        'SELECT t.id, content, created, author_id, username'
        ' FROM todo t JOIN user u ON t.author_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if todo is None:
        abort(404, f"Todo id {id} doesn't exist.") # HTTPステータスコードを返す特別な例外を発生させる

    if check_author and todo['author_id'] != g.user['id']:
        abort(403)

    return todo


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        content = request.form['content']
        error = None

        if not content:
            error = 'Content is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE todo SET content = ?'
                ' WHERE id = ?',
                (content, id)
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/update.html', todo=todo)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_todo(id)
    db = get_db()
    db.execute('DELETE FROM todo WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('todo.index'))


@bp.route('/<int:user_id>')
@login_required
def mytodo(user_id):
    db = get_db()
    todos = db.execute(
        'SELECT t.id, content, created'
        ' FROM todo t JOIN user u ON t.author_id = u.id'
        ' WHERE author_id = ?'
        ' ORDER BY created DESC', (user_id,)
    ).fetchall()
    return render_template('todo/mytodo.html', todos=todos)