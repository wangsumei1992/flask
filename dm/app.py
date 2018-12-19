import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__) # create the application instance :)
# app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'defect.db'),
    SECRET_KEY='development key',
))
app.config.from_envvar('DM_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext #当应用退出的时候
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def get_all_defects():
    db = get_db()
    cur = db.execute('select * from defects order by id desc')
    defects = cur.fetchall() #拿数据
    return render_template('index.html', defects=defects)

@app.route('/new')
def display_create_defect_form():
    return render_template('new.html')