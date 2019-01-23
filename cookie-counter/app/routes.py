import os
import time
import uuid
import logging
from app import app, db
from flask import jsonify, flash, render_template, request, redirect, url_for
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


def unique_filename(filename):
    return time.strftime("%d-%m-%Y") + '-' + uuid.uuid4().hex[:8] + '-' + filename


# ----------------------------- director --------------------------------
@app.route("/anl-admin/director")
def admin_director():
    return render_template('anl-admin-director.html', title='Movie Director')


def hydrate_directors(directors):
    result = []
    for d in directors:
        director = {
            'id': d.id,
            'name_en': d.name_en,
            'name_kr': d.name_kr,
            'photo': d.photo
        }
        result.append(director)
    return result


def get_all_directors():
    return hydrate_directors(Director.query.all())


def hydrate_movies_with_director(movies):
    result = []
    for m in movies:
        movie = {
            'id': m.id,
            'name_en': m.name_en,
            'name_kr': m.name_kr,
            'photo': m.photo
        }
        result.append(movie)
    return result


def get_director_of_all_movies():
    return hydrate_movies_with_director(Movie.query.all())


# TODO : render_template title 'ㅇㅇㅇ 감독의 영화 목록'으로 변경
@app.route('/anl-admin/director/<id>', methods=['GET'])
def director_of_movie(id):
    director = Director.query.filter_by(id=id).first()
    if director is None:
        flash('Director {} not found.'.format(id))
    return render_template('anl-admin-director-movie-search.html', director=director)


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
        db.session.commit()
        return redirect(url_for('admin_director'))
    else:
        form.director_en_name.data = director.name_en
        form.director_kr_name.data = director.name_kr
    return render_template('anl-admin-director-new.html', title='Edit Director Data', form=form,
                           filename=director.photo)


# -------------------------------- director api ---------------------------------
@app.route('/anl-api/director')
def api_director():
    keyword = request.args.get('keyword')
    if keyword is None:
        directors = get_all_directors()
    else:
        condition = Director.name_en.like(f"%{keyword}%")
        condition2 = Director.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        query = Director.query.filter(or_clause).all()
        directors = hydrate_directors(query)

    return jsonify(directors=directors)


@app.route('/anl-api/movie-with-director/<id>', methods=['GET'])
def get_director_of_movie(id):
    keyword = request.args.get('keyword')
    if keyword is None:
        movies = Movie.query.filter(~Movie.directors.any(Director.id==id)).all()
        producers = Movie.query.filter(Movie.directors.any(Director.id==id)).all()
    else:
        condition = Movie.name_en.like(f"%{keyword}%")
        condition2 = Movie.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        movie_query = Movie.query.filter(or_clause)
        movies = movie_query.filter(~Movie.directors.any(Director.id==id)).all()
        producer_query = Movie.query.filter(Movie.directors.any(Director.id==id))
        producers = producer_query.filter(or_clause).all()
    movie_dict = hydrate_movies_with_director(movies)
    producer_dict = hydrate_movies_with_director(producers)
    return jsonify(movies=movie_dict, id=id, producers=producer_dict)


@app.route('/anl-api/movie/<mid>/director/<did>', methods=['POST'])
def associate_movie_with_director(mid, did):
    movie = Movie.query.filter_by(id=mid).first()
    director = Director.query.filter_by(id=did).first()
    movie.directors.append(director)
    db.session.commit()

    return jsonify({
        'status': 'OK'
    })


@app.route('/anl-api/movie/<mid>/director/<did>', methods=['DELETE'])
def remove_director_from_movie(mid, did):
    movie = Movie.query.filter_by(id=mid).first()
    director = Director.query.with_parent(movie).filter_by(id=did).one()
    movie.directors.remove(director)
    db.session.commit()

    return jsonify({
        'status': 'OK'
    })


@app.route('/anl-api/movie-with-director/<id>', methods=['POST'])
def edit_director_of_movie_api(id):
    json = request.get_json()
    name_en = json.get('name_en')
    name_kr = json.get('name_kr')
    director = Director.query.get(id)
    director.name_en = name_en
    director.name_kr = name_kr
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': get_director_of_all_movies()
    })


@app.route('/anl-api/director/<id>', methods=['POST'])
def edit_director_api(id):
    json = request.get_json()
    name_en = json.get('name_en')
    name_kr = json.get('name_kr')
    director = Director.query.get(id)
    director.name_en = name_en
    director.name_kr = name_kr
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': get_all_directors()
    })


@app.route('/anl-api/director/photo/<id>', methods=['POST'])
def change_director_photo(id):
    photo_data = request.files['photo']
    filename = unique_filename(photo_data.filename)
    upload_folder = app.config['UPLOAD_FOLDER']
    photo_data.save(os.path.join(upload_folder, filename))
    director = Director.query.get(id)
    director.photo = filename
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': get_all_directors()
    })


@app.route('/anl-api/director/photo', methods=['POST'])
def delete_director_photo():
    json = request.get_json()
    id = json.get('id')
    director = Director.query.get(id)
    director.photo = None
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': get_all_directors()
    })


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


# ----------------------------- actor --------------------------------

@app.route("/anl-admin/actor")
def admin_actor():
    return render_template('anl-admin-actor.html', title='Movie Actor')


def hydrate_actors(actors):
    result = []
    for a in actors:
        actor = {
            'id': a.id,
            'name_en': a.name_en,
            'name_kr': a.name_kr,
            'photo': a.photo
        }
        result.append(actor)
    return result


def get_all_actors():
    return hydrate_actors(Actor.query.all())


def hydrate_movies_with_actor(movies):
    result = []
    for m in movies:
        movie = {
            'id': m.id,
            'name_en': m.name_en,
            'name_kr': m.name_kr,
            'photo': m.photo
        }
        result.append(movie)
    return result


def get_actor_of_all_movies():
    return hydrate_movies_with_actor(Movie.query.all())


# TODO : render_template title 'ooo 배우의 영화 목록'으로 변경
@app.route('/anl-admin/actor/<id>', methods=['GET'])
def actor_of_movie(id):
    actor = Actor.query.filter_by(id=id).first()
    if actor is None:
        flash('Actor {} not found.'.format(id))
    return render_template('anl-admin-actor-movie-search.html', actor=actor)


@app.route('/anl-admin/actor/new', methods=['GET', 'POST'])
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
        actor.photo = filename
        db.session.add(actor)
        db.session.commit()
        return redirect(url_for('admin_actor'))
    else:
        form.actor_en_name.data = actor.name_en
        form.actor_kr_name.data = actor.name_kr
    return render_template('anl-admin-actor-new.html',
                           title='Register New Actor', form=form, filename=actor.photo)


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
        db.session.commit()
        return redirect(url_for('admin_actor'))
    else:
        form.actor_en_name.data = actor.name_en
        form.actor_kr_name.data = actor.name_kr
    return render_template('anl-admin-actor-new.html', title='Edit Actor Data', form=form, filename=actor.photo)


# ----------------------------- actor api --------------------------------
@app.route("/anl-api/actor")
def api_actor():
    keyword = request.args.get('keyword')
    if keyword is None:
        actors = get_all_actors()
    else:
        condition = Actor.name_en.like(f"%{keyword}%")
        condition2 = Actor.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        query = Actor.query.filter(or_clause).all()
        actors = hydrate_actors(query)

    return jsonify(actors=actors)


@app.route('/anl-api/movie-with-actor/<id>', methods=['GET'])
def get_actor_of_movie(id):
    keyword = request.args.get('keyword')
    if keyword is None:
        movies = Movie.query.filter(~Movie.directors.any(Director.id==id)).all()
        actors = Movie.query.filter(Movie.directors.any(Director.id==id)).all()
    else:
        condition = Movie.name_en.like(f"%{keyword}%")
        condition2 = Movie.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        movie_query = Movie.query.filter(or_clause)
        movies = movie_query.filter(~Movie.actors.any(Actor.id==id)).all()
        actor_query = Movie.query.filter(Movie.actors.any(Actor.id==id))
        actors = actor_query.filter(or_clause).all()
    movie_dict = hydrate_movies_with_actor(movies)
    actor_dict = hydrate_movies_with_actor(actors)
    return jsonify(movies=movie_dict, id=id, actors=actor_dict)


@app.route('/anl-api/movie/<mid>/actor/<aid>', methods=['POST'])
def associate_movie_with_actor(mid, aid):
    movie = Movie.query.filter_by(id=mid).first()
    actor = Actor.query.filter_by(id=aid).first()
    movie.actors.append(actor)
    db.session.commit()

    return jsonify({
        'status': 'OK'
    })


@app.route('/anl-api/movie/<mid>/actor/<aid>', methods=['DELETE'])
def remove_actor_from_movie(mid, aid):
    movie = Movie.query.filter_by(id=mid).first()
    actor = Actor.query.with_parent(movie).filter_by(id=aid).one()
    movie.actors.remove(actor)
    db.session.commit()

    return jsonify({
        'status': 'OK'
    })


@app.route('/anl-api/movie-with-actor/<id>', methods=['POST'])
def edit_actor_of_movie_api(id):
    json = request.get_json()
    name_en = json.get('name_en')
    name_kr = json.get('name_kr')
    actor = Actor.query.get(id)
    actor.name_en = name_en
    actor.name_kr = name_kr
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'actors': get_actor_of_all_movies()
    })


@app.route('/anl-api/actor/<id>', methods=['POST'])
def edit_actor_api(id):
    json = request.get_json()
    name_en = json.get('name_en')
    name_kr = json.get('name_kr')
    actor = Actor.query.get(id)
    actor.name_en = name_en
    actor.name_kr = name_kr
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': get_all_actors()
    })


@app.route('/anl-api/actor/photo/<id>', methods=['POST'])
def change_actor_photo(id):
    photo_data = request.files['photo']
    filename = unique_filename(photo_data.filename)
    upload_folder = app.config['UPLOAD_FOLDER']
    photo_data.save(os.path.join(upload_folder, filename))
    actor = Actor.query.get(id)
    actor.photo = filename
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': get_all_actors()
    })


@app.route('/anl-admin/actor/photo', methods=['POST'])
def delete_actor_photo():
    json = request.get_json()
    id = json.get('id')
    actor = Actor.query.get(id)
    actor.photo = None
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'actors': get_all_actors()
    })


@app.route('/anl-admin/actor/<id>', methods=['DELETE'])
def delete_actor(id):
    actor = Actor.query.get(id)
    db.session.delete(actor)
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'actors': get_all_actors()
    })


# ----------------------------- movie --------------------------------

@app.route("/anl-admin/movie")
def admin_movie():
    return render_template('anl-admin-movie.html', title='Movie')


@app.route('/anl-api/movie')
def api_movie():
    movies = get_all_movies()
    return jsonify(movies=movies)


def get_all_movies():
    movies = []
    for m in Movie.query.all():
        movie = {
            'id': m.id,
            'name_en': m.name_en,
            'name_kr': m.name_kr,
            'photo': m.photo
        }
        movies.append(movie)
    return movies


@app.route('/anl-admin/movie/new', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    movie = Movie(name_kr=form.movie_kr_name.data, name_en=form.movie_en_name.data)

    if request.method == 'POST' and form.validate_on_submit():
        logging.error(form)
        logging.error(form.photo)
        logging.error(form.photo.data)
        photo_data = form.photo.data
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = unique_filename(photo_data.filename)
        photo_data.save(os.path.join(upload_folder, filename))
        movie.photo = filename
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('admin_movie'))
    return render_template('anl-admin-movie-new.html',
                           title='Register New Movie', form=form, filename=movie.photo)


@app.route('/anl-admin/movie/edit/<id>', methods=['GET', 'POST'])
def edit_movie(id):
    form = MovieForm()
    movie = Movie.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        movie.name_en = form.movie_en_name.data
        movie.name_kr = form.movie_kr_name.data
        db.session.commit()
        return redirect(url_for('admin_movie'))
    else:
        form.movie_en_name.data = movie.name_en
        form.movie_kr_name.data = movie.name_kr
    return render_template('anl-admin-movie-new.html', title='Edit Movie Data', form=form)


# ----------------------------- movie api --------------------------------

@app.route('/anl-api/movie/<id>', methods=['POST'])
def edit_movie_api(id):
    json = request.get_json()
    name_en = json.get('name_en')
    name_kr = json.get('name_kr')
    movie = Movie.query.get(id)
    movie.name_en = name_en
    movie.name_kr = name_kr
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'movies': get_all_movies()
    })


@app.route('/anl-api/movie/photo', methods=['POST'])
def delete_movie_photo():
    json = request.get_json()
    id = json.get('id')
    movie = Movie.query.get(id)
    movie.photo = None
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'movies': get_all_movies()
    })


@app.route('/anl-admin/movie/delete/<id>', methods=['GET', 'POST'])
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for('admin_movie'))
