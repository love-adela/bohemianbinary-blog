import json
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


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return {x.name: getattr(obj, x.name) for x in obj.__table__.columns}
        else:
            json.JSONEncoder.default(self, obj)


app.json_encoder = Encoder


# ----------------------------- director --------------------------------
@app.route("/anl-admin/director")
def admin_director():
    return render_template('anl-admin-director.html', title='Movie Director')


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
        directors = Director.query.all()
    else:
        condition = Director.name_en.like(f"%{keyword}%")
        condition2 = Director.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        directors = Director.query.filter(or_clause).all()

    return jsonify(directors=directors)


@app.route('/anl-api/movie-with-director/<id>', methods=['GET'])
def get_director_of_movie(id):
    keyword = request.args.get('keyword')
    if keyword is None:
        movies = Movie.query.filter(~Movie.directors.any(Director.id == id)).all()
        producers = Movie.query.filter(Movie.directors.any(Director.id == id)).all()
    else:
        condition = Movie.name_en.like(f"%{keyword}%")
        condition2 = Movie.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        movie_query = Movie.query.filter(or_clause)
        movies = movie_query.filter(~Movie.directors.any(Director.id == id)).all()
        producer_query = Movie.query.filter(Movie.directors.any(Director.id == id))
        producers = producer_query.filter(or_clause).all()
    return jsonify(movies=movies, producers=producers)


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
    director = Director.query.with_parent(movie).filter_by(id=did).first()
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
        'directors': Director.query.all()
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
        'directors': Director.query.all()
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
        'directors': Director.query.all()
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
        'directors': Director.query.all()
    })


@app.route('/anl-api/director/<id>', methods=['DELETE'])
def delete_director(id):
    director = Director.query.get(id)
    db.session.delete(director)
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': Director.query.all()
    })


# ----------------------------- actor --------------------------------

@app.route("/anl-admin/actor")
def admin_actor():
    return render_template('anl-admin-actor.html', title='Movie Actor')


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
        actors = Actor.query.all()
    else:
        condition = Actor.name_en.like(f"%{keyword}%")
        condition2 = Actor.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        actors = Actor.query.filter(or_clause).all()
    return jsonify(actors=actors)


@app.route('/anl-api/movie-with-actor/<id>', methods=['GET'])
def get_actor_of_movie(id):
    keyword = request.args.get('keyword')
    if keyword is None:
        movies = Movie.query.filter(~Movie.actors.any(Actor.id == id)).all()
        actors = Movie.query.filter(Movie.actors.any(Actor.id == id)).all()
    else:
        condition = Movie.name_en.like(f"%{keyword}%")
        condition2 = Movie.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        movie_query = Movie.query.filter(or_clause)
        movies = movie_query.filter(~Movie.actors.any(Actor.id == id)).all()
        actor_query = Movie.query.filter(Movie.actors.any(Actor.id == id))
        actors = actor_query.filter(or_clause).all()
    return jsonify(movies=movies, id=id, actors=actors)


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
    actor = Actor.query.with_parent(movie).filter_by(id=aid).first()
    if movie is None:
        return jsonify({
            'status': "ERROR",
            'message': "No movie was found."
        })
    if actor is None:
        return jsonify({
            'status': "ERROR",
            'message': "No actor was found."
        })
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
        'actors': Actor.query.all()
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
        'actors': Actor.query.all()
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
        'actors': Actor.query.all()
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
        'actors': Actor.query.all()
    })


@app.route('/anl-admin/actor/<id>', methods=['DELETE'])
def delete_actor(id):
    actor = Actor.query.get(id)
    db.session.delete(actor)
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'actors': Actor.query.all()
    })


# ----------------------------- movie --------------------------------

@app.route("/anl-admin/movie")
def admin_movie():
    return render_template('anl-admin-movie.html', title='Movie')


@app.route('/anl-admin/movie/<mid>', methods=['GET'])
def get_movie_information(mid):
    movie = Movie.query.filter_by(id=mid).first()
    if movie is None:
        flash('Movie {} not found.'.format(mid))
    return render_template('anl-admin-movie-cookie.html', movie=movie, mid=mid)


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


@app.route('/anl-admin/movie/delete/<id>', methods=['GET', 'POST'])
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('admin_movie'))


# ----------------------------- movie api --------------------------------
@app.route('/anl-api/movie')
def get_api_movie():
    keyword = request.args.get('keyword')
    if keyword is None:
        movies = Movie.query.all()
    else:
        condition = Movie.name_en.like(f"%{keyword}%")
        condition2 = Movie.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        movies = Movie.query.filter(or_clause).all()
    return jsonify(movies=movies)


@app.route('/anl-api/movie/<mid>', methods=['GET'])
def get_this_movie_api(mid):
    movie = Movie.query.filter_by(id=mid).first()
    return jsonify({
        'id': movie.id,
        'name_en': movie.name_en,
        'name_kr': movie.name_kr,
        'number_of_cookies': movie.number_of_cookies,
        'photo': movie.photo,
        'directors': movie.directors,
        'actors': movie.actors
    })


@app.route('/anl-api/movie/<mid>', methods=['POST'])
def edit_movie_api(mid):
    json = request.get_json()
    name_en = json.get('name_en')
    name_kr = json.get('name_kr')
    number_of_cookies = json.get('number_of_cookies')

    movie = Movie.query.get(mid)
    movie.name_en = name_en
    movie.name_kr = name_kr
    movie.number_of_cookies = number_of_cookies
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': mid,
        'movies': Movie.query.all(),
        'number_of_cookies': number_of_cookies
    })


@app.route('/anl-api/movie/<mid>/cookie', methods=["GET"])
def show_modified_number_of_cookies(mid):
    movie = Movie.query.get(mid)
    return jsonify({
        'id': mid,
        'number_of_cookies': movie.number_of_cookies
    })


@app.route('/anl-api/movie/<mid>/cookie', methods=["POST"])
def modify_number_of_cookies(mid):
    json = request.get_json()
    number_of_cookies = json.get('number_of_cookies')
    movie = Movie.query.get(mid)
    movie.number_of_cookies = number_of_cookies
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': mid,
        'movie': {
            'id': movie.id,
            'name_en': movie.name_en,
            'name_kr': movie.name_kr,
            'photo': movie.photo,
            'number_of_cookies': movie.number_of_cookies,
            'directors': movie.directors,
            'actors': movie.actors
        }
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
        'movies': Movie.query.all()
    })
