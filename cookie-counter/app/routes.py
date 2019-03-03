from app import app, db
from flask import render_template


@app.route('/')
def base():
    return render_template('base.html', title='Home')


@app.route('/index')
def index():
    return render_template('index.html', title='Main')
