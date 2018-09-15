from app import app, db
from app.models import Actor, Director
from app.forms import ActorForm, DirectorForm
from flask import flash, render_template, request, redirect, url_for

import os
import time
import uuid


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


def unique_filename(filename):
    return time.strftime("%d-%m-%Y") + '-' + uuid.uuid4().hex[:8] + '-' + filename


# 새로운 감독 데이터 등록
@app.route('/anl-admin/director/new', methods=['GET', 'POST'])
def add_director():
    form = DirectorForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
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
    return render_template('anl-admin-director-new.html', title='Edit New Director', form=form, filename=director.photo)


# 감독 데이터 삭제
@app.route('/anl-admin/director/delete/<id>', methods=['GET', 'POST'])
def delete_director(id):
    director = Director.query.get(id)
    db.session.delete(director)
    db.session.commit()

    return redirect(url_for('admin_director'))


@app.route("/anl-admin/actor")
def admin_actor():
    actors = Actor.query.all()
    return render_template('anl-admin-actor.html', title='Movie Actor', actors=actors)


# 새로운 배우 데이터 등록
@app.route("/anl-admin/actor/new", methods=['GET', 'POST'])
def add_actor():
    form = ActorForm()
    if form.validate_on_submit():
        flash('Register {} ({})'.format(form.actor_kr_name.data, form.actor_en_name.data))

        actor = Actor(name_kr=form.actor_kr_name.data, name_en=form.actor_en_name.data)
        db.session.add(actor)
        db.session.commit()

        return redirect(url_for('admin_actor'))

    return render_template('anl-admin-actor-new.html', title='Register New Actor', form=form)


# 배우 데이터 수정
@app.route('/anl-admin/actor/edit/<id>', methods=['GET', 'POST'])
def edit_actor(id):
    form = DirectorForm()
    actor = Actor.query.get(id)

    if request.method == 'POST' and form.validate_on_submit():
        actor.name_en = form.actor_en_name.data
        actor.name_kr = form.actor_kr_name.data
        db.session.add(actor)
        db.session.commit()
        return redirect(url_for('admin_actor'))
    else:
        form.actor_en_name.data = actor.name_en
        form.actor_kr_name.data = actor.name_kr
    return render_template('anl-admin-actor-new.html', title='Edit New Actor', form=form)


# 배우 데이터 삭제
@app.route('/anl-admin/actor/delete/<id>', methods=['GET', 'POST'])
def delete_actor(id):
    actor = Actor.query.get(id)
    db.session.delete(actor)
    db.session.commit()

    return redirect(url_for('admin_actor'))


@app.route('/anl-admin/movie')
def admin_movie():
    movies = [
        {'name': 'Searching'},
        {'name': 'Incredibles2'},
        {'name': 'Mission : Impossible - Fallout'}

    ]
    return render_template('anl-admin-movie.html', title='Movie', movies=movies)

