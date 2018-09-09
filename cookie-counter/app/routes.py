from flask import render_template, request, redirect, flash, redirect, url_for
from app import app
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
    directors = [
        {'name': 'Aneesh Chaganty'},
        {'name': 'Brad Bird'},
        {'name': 'Christopher McQuarrie'},

    ]
    return render_template('anl-admin-director.html', title='Movie Director', directors=directors)


@app.route('/anl-admin/director/new', methods=['POST'])
def add_director():
    form = DirectorForm()
    if form.validate_on_submit():
        flash('Register {}'.format(form.directorname.data))
        return redirect(url_for('/index'))
    return render_template('anl-admin-director-new.html', title='Register New Director', form=form)


@app.route('/anl-admin/movie')
def admin_movie():
    movies = [
        {'name': 'Searching'},
        {'name': 'Incredibles2'},
        {'name': 'Mission : Impossible - Fallout'}

    ]
    return render_template('anl-admin-movie.html', title='Movie', movies=movies)


@app.route("/anl-admin/actor")
def admin_actor():
    actors = [
        {'name': 'John Cho'},
        {'name': 'Craig T.Nelson'},
        {'name': 'Tom Cruise'},

    ]
    return render_template('anl-admin-actor.html', title='Movie Actor', actors=actors)

