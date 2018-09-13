from flask import render_template, request, redirect, flash, redirect, url_for
from app import app, db
from app.models import Director
from app.forms import DirectorForm


@app.route('/')
def base():
    return render_template('base.html', title='Home')


@app.route('/index')
def index():
    return render_template('index.html', title='Main')


@app.route('/anl-admin')
def admin_main():
    return "The delicious way to count movie cookies!"


@app.route("/anl-admin/director")
def admin_director():
    directors = Director.query.all()
    return render_template('anl-admin-director.html', title='Movie Director', directors=directors)


# 새로운 감독 데이터 등록
@app.route('/anl-admin/director/new', methods=['GET', 'POST'])
def add_director():
    form = DirectorForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        flash('Register {} ({})'.format(form.director_kr_name.data, form.director_en_name.data))

        director = Director(name_kr=form.director_kr_name.data, name_en=form.director_en_name.data)
        db.session.add(director)
        db.session.commit()

        return redirect(url_for('admin_director'))
    return render_template('anl-admin-director-new.html', title='Register New Director', form=form)


# 감독 데이터 수정
@app.route('/anl-admin/director/edit/<id>', methods=['GET', 'POST'])
def edit_director(id):
    form = DirectorForm()
    director = Director.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        director.name_en = form.director_en_name.data
        director.name_kr = form.director_kr_name.data
        db.session.add(director)
        db.session.commit()
        return redirect(url_for('admin_director'))
    else:
        form.director_en_name.data = director.name_en
        form.director_kr_name.data = director.name_kr
    return render_template('anl-admin-director-new.html', title='Edit New Director', form=form)


# 감독 데이터 삭제
@app.route('/anl-admin/director/delete/<id>', methods=['GET', 'POST'])
def delete_director(id):
    if request.method == 'POST':
        director = Director.query.get(id)
        db.session.delete(director)
        db.session.commit()

    return redirect(url_for('admin_director'))


@app.route("/anl-admin/actor")
def admin_actor():
    actors = [
        {'name': 'John Cho'},
        {'name': 'Craig T.Nelson'},
        {'name': 'Tom Cruise'},

    ]
    return render_template('anl-admin-actor.html', title='Movie Actor', actors=actors)

#
# # 새로운 배우 데이터 등록
# @app.route("/anl-admin/actor/new", methods=['GET', 'POST'])
# def add_actor():
#     form = ActorForm()
#     if form.validate_on_submit():
#         flash('Register {} ({})'.format(form.actor_kr_name.data, form.actor_en_name.data))
#
#         actor = Actor(name_kr=form.actor_kr_name.data, name_en=form.actor_en_name.data)
#         db.session.add(actor)
#         db.session.commit()

#
# # 배우 데이터 수정
# @app.route('/anl-admin/actor/edit', methods=['GET', 'POST'])

@app.route('/anl-admin/movie')
def admin_movie():
    movies = [
        {'name': 'Searching'},
        {'name': 'Incredibles2'},
        {'name': 'Mission : Impossible - Fallout'}

    ]
    return render_template('anl-admin-movie.html', title='Movie', movies=movies)


