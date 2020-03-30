from flask import Blueprint, render_template, request

from . import db


bp = Blueprint("todos", __name__)

@bp.route("/", methods=('GET', 'POST'))
def index():
    """View for home page which shows list of to-do items."""

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


    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)
