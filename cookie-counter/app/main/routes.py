from flask import render_template

from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
def base():
    return render_template('base.html', title='Home')
