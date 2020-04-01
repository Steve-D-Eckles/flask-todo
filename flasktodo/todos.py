from flask import Blueprint, g, redirect, render_template, session, request, url_for

from . import db
from flasktodo.auth import login_required


bp = Blueprint("todos", __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    """View for home page which shows list of to-do items."""

    if request.method == 'POST':
        session['filter'] = request.form['filter']

    todos = []

    if g.user:
        cur = db.get_db().cursor()

        if not session.get('filter') or session.get('filter') == 'all':
            cur.execute('SELECT * FROM todos WHERE user_id = %s', (g.user['id'],))
        elif session['filter'] == 'completed':
            cur.execute('SELECT * FROM todos WHERE completed = true AND user_id = %s', (g.user['id'],))
        else:
            cur.execute('SELECT * FROM todos WHERE completed = false AND user_id = %s', (g.user['id'],))

        todos = cur.fetchall()
        cur.close()

    return render_template("index.html", todos=todos)

@bp.route('/toggle', methods=('GET', 'POST'))
@login_required
def toggle():
    """Endpoint for toggling list items; redirect to index"""
    if request.method == 'POST':
        with db.get_db() as con:
            with con.cursor() as cur:
                for item in request.form:
                    cur.execute("""
                        SELECT completed FROM todos
                        WHERE id = %s
                    """, (request.form[item],))
                    toggle = cur.fetchone()[0]
                    cur.execute("""
                        UPDATE todos
                        SET completed = %s
                        WHERE id = %s AND user_id = %s
                    """, (False if toggle else True, request.form[item], g.user['id']))

    return redirect(url_for('todos.index'))

@bp.route('/new-todo', methods=('GET', 'POST'))
@login_required
def new():
    """Endpoint for filtering list items; redirect to index"""
    if request.method == 'POST':
        newitem = request.form['new-item']
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("INSERT INTO todos (description, completed, created_at, user_id) VALUES (%s, %s, NOW(), %s)",
                                (newitem, False, g.user['id'])
                            )

    return redirect(url_for("todos.index"))

@bp.route('/remove', methods=('GET', 'POST'))
@login_required
def remove():
    """Endpoint for removing list items; redirect to index"""
    if request.method == 'POST':
        with db.get_db() as con:
            with con.cursor() as cur:
                for item in request.form:
                    cur.execute("""
                        DELETE FROM todos
                        WHERE id = %s
                    """, (request.form[item],))

    return redirect(url_for('todos.index'))
