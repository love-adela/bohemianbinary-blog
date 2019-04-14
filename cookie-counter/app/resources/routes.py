from flask import jsonify, request
from app.models import Movie
from app.resources import bp

# ----------------------------- movie api --------------------------------

@bp.route('/api/movie', methods=['GET'])
def get_api_movie():
    keyword = request.args.get('keyword')
    before = request.args.get('before')
    after = request.args.get('after')
    count = request.args.get('count')
    limit = request.args.get('limit')
    if keyword is None:
        movies = Movie.query.all()

    if before is not None:
        before = int(before, 16)

    if after is not None:
        after = int(after, 16)

    if count is None:
        movies = Movie.query.all()

    if limit is None:
        movies = Movie.query.all()

    else:
        condition = Movie.name_en.like(f"%{keyword}%")
        condition2 = Movie.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        movies = Movie.query.filter(or_clause).all()

        if before is not None:
            movies = movies.filter(Movie.id <= before).limit(10)

        if after is not None:
            movies = movies.filter(Movie.id >= after).order_by(Movie.id.desc()).limit(10)

        movies =movies.all()
    return jsonify(movies=movies)
