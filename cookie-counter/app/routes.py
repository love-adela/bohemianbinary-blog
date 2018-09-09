from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route("/admin-anl/director")
def admin_anl():
    movie = [
        {'movie_name':'Searching'},
        {'movie_name': 'The Predator'},
        {'movie_name': 'Mission : Impossible - Fallout'}

    ]
    director = [
        {'director_name' : 'Aneesh Chaganty'},
        {'director_name': 'Shane Black'},
        {'director_name': 'Christopher McQuarrie'},

    ]
    return render_template('admin-anl.html', title='Movie Director', movie=movie, director=director)

