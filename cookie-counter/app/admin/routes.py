import os
import time
import uuid
from flask import current_app, jsonify, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from app.admin import bp
from app.admin.forms import ActorForm, DirectorForm, MovieForm, LoginForm, RegistrationForm
from app.models import Director, Actor, Movie, Admin


def unique_filename(filename):
    return time.strftime("%d-%m-%Y") + '-' + uuid.uuid4().hex[:8] + '-' + filename


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Main')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.username.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin.login'))
        login_user(admin, remember=form.remember_me.data)
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        admin = Admin(name=form.username.data, email=form.email.data)
        admin.set_password(form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('admin.login'))
    return render_template('admin/register.html', title='Register', form=form)


# ----------------------------- director --------------------------------
@bp.route("/director")
@login_required
def admin_director():
    return render_template('anl-admin-director.html', title='Movie Director')


@bp.route('/director/<id>', methods=['GET'])
@login_required
def director_of_movie(id):
    director = Director.query.filter_by(id=id).first()
    if director is None:
        flash('Director {} not found.'.format(id))
    return render_template('anl-admin-director-movie-search.html', director=director)


@bp.route('/director/new', methods=['GET', 'POST'])
@login_required
def add_director():
    form = DirectorForm()
    director = Director(name_kr=form.director_kr_name.data, name_en=form.director_en_name.data)

    if request.method == 'POST' and form.validate_on_submit():
        photo_data = form.photo.data
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = unique_filename(photo_data.filename)
        photo_data.save(os.path.join(upload_folder, filename))

        director.photo = filename
        db.session.add(director)
        db.session.commit()
        return redirect(url_for('admin.admin_director'))
    else:
        form.director_en_name.data = director.name_en
        form.director_kr_name.data = director.name_kr
    return render_template('anl-admin-director-new.html',
                           title='Register New Director', form=form, filename=director.photo)


@bp.route('/director/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_director(id):
    form = DirectorForm()
    director = Director.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        photo_data = form.photo.data
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = unique_filename(photo_data.filename)
        photo_data.save(os.path.join(upload_folder, filename))

        director.name_en = form.director_en_name.data
        director.name_kr = form.director_kr_name.data
        director.photo = filename
        db.session.commit()
        return redirect(url_for('admin.admin_director'))
    else:
        form.director_en_name.data = director.name_en
        form.director_kr_name.data = director.name_kr
    return render_template('anl-admin-director-new.html', title='Edit Director Data', form=form,
                           filename=director.photo)


# -------------------------------- director api ---------------------------------
@bp.route('/api/director')
@login_required
def api_director():
    keyword = request.args.get('keyword')
    if keyword is None:
        directors = Director.query.all()
    else:
        condition = Director.name_en.like(f"{keyword}")
        condition2 = Director.name_kr.like(f"{keyword}")
        or_clause = (condition | condition2)
        directors = Director.query.filter(or_clause).all()

    return jsonify(directors=directors)


@bp.route('/api/movie-with-director/<id>', methods=['GET'])
@login_required
def get_director_of_movie(id):
    keyword = request.args.get('keyword')
    if keyword is None:
        movies = Movie.query.filter(~Movie.directors.any(Director.id == id)).all()
        producers = Movie.query.filter(Movie.directors.any(Director.id == id)).all()
    else:
        condition = Movie.name_en.like(f"{keyword}")
        condition2 = Movie.name_kr.like(f"{keyword}")
        or_clause = (condition | condition2)
        movie_query = Movie.query.filter(or_clause)
        movies = movie_query.filter(~Movie.directors.any(Director.id == id)).all()
        producer_query = Movie.query.filter(Movie.directors.any(Director.id == id))
        producers = producer_query.filter(or_clause).all()
    return jsonify(movies=movies, producers=producers)


@bp.route('/api/movie/<mid>/director/<did>', methods=['POST'])
@login_required
def associate_movie_with_director(mid, did):
    movie = Movie.query.filter_by(id=mid).first()
    director = Director.query.filter_by(id=did).first()
    movie.directors.append(director)
    db.session.commit()

    return jsonify({
        'status': 'OK'
    })


@bp.route('/api/movie/<mid>/director/<did>', methods=['DELETE'])
@login_required
def remove_director_from_movie(mid, did):
    movie = Movie.query.filter_by(id=mid).first()
    director = Director.query.with_parent(movie).filter_by(id=did).first()
    movie.directors.remove(director)
    db.session.commit()

    return jsonify({
        'status': 'OK'
    })


@bp.route('/api/movie-with-director/<id>', methods=['POST'])
@login_required
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


@bp.route('/api/director/<id>', methods=['POST'])
@login_required
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


@bp.route('/api/director/photo/<id>', methods=['POST'])
@login_required
def change_director_photo(id):
    photo_data = request.files['photo']
    filename = unique_filename(photo_data.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    photo_data.save(os.path.join(upload_folder, filename))
    director = Director.query.get(id)
    director.photo = filename
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'directors': Director.query.all()
    })


@bp.route('/api/director/photo', methods=['POST'])
@login_required
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


@bp.route('/api/director/<id>', methods=['DELETE'])
@login_required
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

@bp.route("/actor")
@login_required
def admin_actor():
    return render_template('anl-admin-actor.html', title='Movie Actor')


@bp.route('/actor/<id>', methods=['GET'])
@login_required
def actor_of_movie(id):
    actor = Actor.query.filter_by(id=id).first()
    if actor is None:
        flash('Actor {} not found.'.format(id))
    return render_template('anl-admin-actor-movie-search.html', actor=actor)


@bp.route('/actor/new', methods=['GET', 'POST'])
@login_required
def add_actor():
    form = ActorForm()
    actor = Actor(name_kr=form.actor_kr_name.data, name_en=form.actor_en_name.data)

    if request.method == 'POST' and form.validate_on_submit():
        photo_data = form.photo.data
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = unique_filename(photo_data.filename)
        photo_data.save(os.path.join(upload_folder, filename))
        actor.photo = filename
        db.session.add(actor)
        db.session.commit()
        return redirect(url_for('admin.admin_actor'))
    else:
        form.actor_en_name.data = actor.name_en
        form.actor_kr_name.data = actor.name_kr
    return render_template('anl-admin-actor-new.html',
                           title='Register New Actor', form=form, filename=actor.photo)


@bp.route('/actor/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_actor(id):
    form = ActorForm()
    actor = Actor.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        photo_data = form.photo.data
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = unique_filename(photo_data.filename)
        photo_data.save(os.path.join(upload_folder, filename))

        actor.name_en = form.actor_en_name.data
        actor.name_kr = form.actor_kr_name.data
        actor.photo = filename
        db.session.commit()
        return redirect(url_for('admin.admin_actor'))
    else:
        form.actor_en_name.data = actor.name_en
        form.actor_kr_name.data = actor.name_kr
    return render_template('anl-admin-actor-new.html', title='Edit Actor Data', form=form, filename=actor.photo)


# ----------------------------- actor api --------------------------------
@bp.route("/api/actor")
@login_required
def api_actor():
    keyword = request.args.get('keyword')
    if keyword is None:
        actors = Actor.query.all()
    else:
        condition = Actor.name_en.like(f"{keyword}")
        condition2 = Actor.name_kr.like(f"{keyword}")
        or_clause = (condition | condition2)
        actors = Actor.query.filter(or_clause).all()
    return jsonify(actors=actors)


@bp.route('/api/movie-with-actor/<id>', methods=['GET'])
@login_required
def get_actor_of_movie(id):
    keyword = request.args.get('keyword')
    if keyword is None:
        movies = Movie.query.filter(~Movie.actors.any(Actor.id == id)).all()
        actors = Movie.query.filter(Movie.actors.any(Actor.id == id)).all()
    else:
        condition = Movie.name_en.like(f"{keyword}")
        condition2 = Movie.name_kr.like(f"{keyword}")
        or_clause = (condition | condition2)
        movie_query = Movie.query.filter(or_clause)
        movies = movie_query.filter(~Movie.actors.any(Actor.id == id)).all()
        actor_query = Movie.query.filter(Movie.actors.any(Actor.id == id))
        actors = actor_query.filter(or_clause).all()
    return jsonify(movies=movies, id=id, actors=actors)


@bp.route('/api/movie/<mid>/actor/<aid>', methods=['POST'])
@login_required
def associate_movie_with_actor(mid, aid):
    movie = Movie.query.filter_by(id=mid).first()
    actor = Actor.query.filter_by(id=aid).first()
    movie.actors.append(actor)
    db.session.commit()

    return jsonify({
        'status': 'OK'
    })


@bp.route('/api/movie/<mid>/actor/<aid>', methods=['DELETE'])
@login_required
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


@bp.route('/api/movie-with-actor/<id>', methods=['POST'])
@login_required
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


@bp.route('/api/actor/<id>', methods=['POST'])
@login_required
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


@bp.route('/api/actor/photo/<id>', methods=['POST'])
@login_required
def change_actor_photo(id):
    photo_data = request.files['photo']
    filename = unique_filename(photo_data.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    photo_data.save(os.path.join(upload_folder, filename))
    actor = Actor.query.get(id)
    actor.photo = filename
    db.session.commit()

    return jsonify({
        'isConfirmed': 'success',
        'id': id,
        'actors': Actor.query.all()
    })


@bp.route('/actor/photo', methods=['POST'])
@login_required
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


@bp.route('/actor/<id>', methods=['DELETE'])
@login_required
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

@bp.route("/movie")
@login_required
def admin_movie():
    return render_template('anl-admin-movie.html', title='Movie')


@bp.route('/movie/<mid>', methods=['GET'])
@login_required
def get_movie_information(mid):
    movie = Movie.query.filter_by(id=mid).first()
    if movie is None:
        flash('Movie {} not found.'.format(mid))
    return render_template('anl-admin-movie-cookie.html', movie=movie, mid=mid)


@bp.route('/movie/new', methods=['GET', 'POST'])
@login_required
def add_movie():
    form = MovieForm()
    movie = Movie(name_kr=form.movie_kr_name.data, name_en=form.movie_en_name.data)

    if request.method == 'POST' and form.validate_on_submit():
        photo_data = form.photo.data
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = unique_filename(photo_data.filename)
        photo_data.save(os.path.join(upload_folder, filename))
        movie.photo = filename
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('admin.admin_movie'))
    return render_template('anl-admin-movie-new.html',
                           title='Register New Movie', form=form, filename=movie.photo)


@bp.route('/movie/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_movie(id):
    form = MovieForm()
    movie = Movie.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        movie.name_en = form.movie_en_name.data
        movie.name_kr = form.movie_kr_name.data
        db.session.commit()
        return redirect(url_for('admin.admin_movie'))
    else:
        form.movie_en_name.data = movie.name_en
        form.movie_kr_name.data = movie.name_kr
    return render_template('anl-admin-movie-new.html', title='Edit Movie Data', form=form)


@bp.route('/movie/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for('admin.admin_movie'))


# ----------------------------- movie api --------------------------------
@bp.route('/api/movie')
@login_required
def get_api_movie():
    keyword = request.args.get('keyword')
    if keyword is None:
        movies = Movie.query.all()
    else:
        condition = Movie.name_en.like(f"{keyword}")
        condition2 = Movie.name_kr.like(f"{keyword}")
        or_clause = (condition | condition2)
        movies = Movie.query.filter(or_clause).all()
    return jsonify(movies=movies)


@bp.route('/api/movie/<mid>', methods=['GET'])
@login_required
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


@bp.route('/api/movie/<mid>', methods=['POST'])
@login_required
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


@bp.route('/api/movie/<mid>/cookie', methods=["GET"])
@login_required
def show_modified_number_of_cookies(mid):
    movie = Movie.query.get(mid)
    return jsonify({
        'id': mid,
        'number_of_cookies': movie.number_of_cookies
    })


@bp.route('/api/movie/<mid>/cookie', methods=["POST"])
@login_required
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


@bp.route('/api/movie/photo', methods=['POST'])
@login_required
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
