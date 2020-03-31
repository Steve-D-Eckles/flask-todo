from flask import Blueprint, redirect, render_template, request, url_for

from . import db


bp = Blueprint("todos", __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    """View for home page which shows list of to-do items."""

    if request.method == 'POST':
        newitem = request.form['new-item']
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("INSERT INTO todos (description, completed, created_at) VALUES (%s, %s, NOW())",
                                (newitem, False)
                            )
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)

@bp.route('/toggle', methods=('GET', 'POST'))
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
                        WHERE id = %s
                    """, (False if toggle else True, request.form[item]))

    return redirect(url_for('todos.index'))

@bp.route('/remove', methods=('GET', 'POST'))
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
