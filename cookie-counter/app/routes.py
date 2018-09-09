from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route("/admin-anl/director")
def admin_anl():
    movie = {'movie_name':'Searching'}
    director = {'director_name' : 'Aneesh Chaganty'}
    return '''
<html>
    <head>
        <title>Director List</title>
    </head>
    <body>
        <h1>Director of ''' + movie['name'] + ''' is ''' + director['name'] + '''</h1>
    </body>
</html>
    '''

