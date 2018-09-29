import os
import time
import uuid
from app import app, db
from flask import flash, jsonify, render_template, request, redirect, url_for
from app.models import Director, Actor, Movie
from app.forms import DirectorForm, ActorForm, MovieForm


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
    return render_template('anl-admin-director.html', title='Movie Director')


def unique_filename(filename):
    return time.strftime("%d-%m-%Y") + '-' + uuid.uuid4().hex[:8] + '-' + filename


@app.route('/anl-api/director')
def api_director():
    directors = get_all_directors()
    return jsonify(directors=directors)


def get_all_directors():
    directors = []
    for d in Director.query.all():
        director = {
            'id': d.id,
            'name_en': d.name_en,
            'name_kr': d.name_kr,
            'photo': d.photo
        }
        directors.append(director)
    return directors


# 새로운 감독 데이터 등록
@app.route('/anl-admin/director/new', methods=['GET', 'POST'])
def add_director():
    form = DirectorForm()
    director = Director(name_kr=form.director_kr_name.data, name_en=form.director_en_name.data)

    if request.method == 'POST' and form.validate_on_submit():
        photo_data = form.photo.data
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = unique_filename(photo_data.filename)
        photo_data.save(os.path.join(upload_folder, filename))
        director.photo = filename
        db.session.add(director)
        db.session.commit()
        return redirect(url_for('admin_director'))
    else:
        form.director_en_name.data = director.name_en
        form.director_kr_name.data = director.name_kr
    return render_template('anl-admin-director-new.html',
                           title='Register New Director', form=form, filename=director.photo)


@app.route('/anl-admin/director/edit/<id>', methods=['GET', 'POST'])
def edit_director(id):
    form = DirectorForm()
    director = Director.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        photo_data = form.photo.data
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = unique_filename(photo_data.filename)
        photo_data.save(os.path.join(upload_folder, filename))

        director.name_en = form.director_en_name.data
        director.name_kr = form.director_kr_name.data
        director.photo = filename
        db.session.add(director)
        db.session.commit()
        return redirect(url_for('admin_director'))
    else:
        form.director_en_name.data = director.name_en
        form.director_kr_name.data = director.name_kr
    return render_template('anl-admin-director-new.html', title='Edit Director Data', form=form, filename=director.photo)


# 감독 데이터 수정 - 사진 제외
@app.route('/anl-api/director/<id>', methods=['POST'])
def edit_director_api(id):
    json = request.get_json()
    name_en = json.get('name_en')
    name_kr = json.get('name_kr')
    director = Director.query.get(id)
    director.name_en = name_en
    director.name_kr = name_kr
    db.session.add(director)
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': get_all_directors()
    })


# 감독 사진 변경


# 감독 사진 삭제
@app.route('/anl-api/director/photo', methods=['POST'])
def delete_director_photo():
    json = request.get_json()
    id = json.get('id')
    director = Director.query.get(id)
    director.photo = None
    db.session.add(director)
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': get_all_directors()
    })


# 감독 항목 삭제
@app.route('/anl-api/director/<id>', methods=['DELETE'])
def delete_director(id):
    director = Director.query.get(id)
    db.session.delete(director)
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': get_all_directors()
    })


@app.route("/anl-admin/actor")
def admin_actor():
    return render_template('anl-admin-actor.html', title='Movie Actor')


@app.route("/anl-api/actor")
def api_actor():
    actors = []
    for a in Actor.query.all():
        actor = {
            'name_en': a.name_en,
            'name_kr': a.name_kr,
            'photo': a.photo
        }
        actors.append(actor)
    return jsonify(actors=actors)


# 새로운 배우 데이터 등록
@app.route("/anl-admin/actor/new", methods=['GET', 'POST'])
def add_actor():
    form = ActorForm()
    actor = Actor(name_kr=form.actor_kr_name.data, name_en=form.actor_en_name.data)

    if request.method == 'POST' and form.validate_on_submit():
        photo_data = form.photo.data
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = unique_filename(photo_data.filename)
        photo_data.save(os.path.join(upload_folder, filename))

        actor.name_en = form.actor_en_name.data
        actor.name_kr = form.actor_kr_name.data
        actor.photo = filename
        db.session.add(actor)
        db.session.commit()
        return redirect(url_for('admin_actor'))

    return render_template('anl-admin-actor-new.html', title='Register New Actor', form=form)


# 배우 데이터 수정
@app.route('/anl-admin/actor/edit/<id>', methods=['GET', 'POST'])
def edit_actor(id):
    form = ActorForm()
    actor = Actor.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        photo_data = form.photo.data
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = unique_filename(photo_data.filename)
        photo_data.save(os.path.join(upload_folder, filename))

        actor.name_en = form.actor_en_name.data
        actor.name_kr = form.actor_kr_name.data
        actor.photo = filename
        db.session.add(actor)
        db.session.commit()
        return redirect(url_for('admin_actor'))
    else:
        form.actor_en_name.data = actor.name_en
        form.actor_kr_name.data = actor.name_kr
    return render_template('anl-admin-actor-new.html', title='Edit Actor Data', form=form, filename=actor.photo)


# 배우 데이터 삭제
@app.route('/anl-admin/actor/delete/<id>', methods=['GET', 'POST'])
def delete_actor(id):
    actor = Actor.query.get(id)
    db.session.delete(actor)
    db.session.commit()

    return redirect(url_for('admin_actor'))


@app.route("/anl-admin/movie")
def admin_movie():
    return render_template('anl-admin-movie.html', title='Movie')


def unique_filename(filename):
    return time.strftime("%d-%m-%Y") + '-' + uuid.uuid4().hex[:8] + '-' + filename


@app.route('/anl-api/movie')
def api_movie():
    movies = []
    for m in Movie.query.all():
        movie = {
            'name_en': m.name_en,
            'name_kr': m.name_kr,
            'photo': m.photo
        }
        movies.append(movie)
    return jsonify(movies=movies)


# 새로운 영화 데이터 등록
@app.route('/anl-admin/movie/new', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        flash('Register {} ({})'.format(form.movie_kr_name.data, form.movie_en_name.data))

        movie = Movie(name_kr=form.movie_kr_name.data, name_en=form.movie_en_name.data)
        db.session.add(movie)
        db.session.commit()

        return redirect(url_for('admin_movie'))
    return render_template('anl-admin-movie-new.html', title='Register New Movie', form=form)


# 영화 데이터 수정
@app.route('/anl-admin/movie/edit/<id>', methods=['GET', 'POST'])
def edit_movie(id):
    form = MovieForm()
    movie = Movie.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        movie.name_en = form.movie_en_name.data
        movie.name_kr = form.movie_kr_name.data
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('admin_movie'))
    else:
        form.movie_en_name.data = movie.name_en
        form.movie_kr_name.data = movie.name_kr
    return render_template('anl-admin-movie-new.html', title='Edit Movie Data', form=form)


# 영화 데이터 삭제
@app.route('/anl-admin/movie/delete/<id>', methods=['GET', 'POST'])
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for('admin_movie'))
