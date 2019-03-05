from flask import render_template
from flask_login import login_required

from app import app, db
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
def base():
    return render_template('base.html', title='Home')

#
# @bp.route('/index', methods=['GET', 'POST'])
#
# def index():
#     return render_template('index.html', title='Main')

