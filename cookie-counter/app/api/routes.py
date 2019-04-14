from flask import jsonify, request

from app.api import bp
from app.models import Movie


@bp.route('/movie', methods=['GET'])
def get_api_movie():
    keyword = request.args.get('keyword')

    if keyword is None:
        movies = Movie.query.all()
    else:
        condition = Movie.name_en.like(f"%{keyword}%")
        condition2 = Movie.name_kr.like(f"%{keyword}%")
        or_clause = (condition | condition2)
        movies = Movie.query.filter(or_clause).all()

    result = {
        "count": len(movies),
        "movies": movies
    }
    return jsonify(result)
