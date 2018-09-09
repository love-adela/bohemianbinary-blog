from flask import render_template
from app import app


@app.route('/')
def index():
    return "Hello World"

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
    return render_template('admin-anl-director.html', title='Movie Director', directors=directors)


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
    return render_template('admin-anl-actor.html', title='Movie Actor', actors=actors)

