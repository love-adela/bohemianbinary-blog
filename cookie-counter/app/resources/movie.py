from flask import request
from flask_restful import Resource
from app.models import db, Movie, MovieSchema

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


class MovieSchema(Resource):
    def get(self):
        movies = Movie.query.all()
        movies = movies_schema.dump(movies).data
        return {'status': 'success', 'data': movies}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        data, errors = movie_schema.load(json_data)
        if errors:
            return errors, 422
        movie = Movie.query.filter_by(name=data['name_kr']).first()
        if movie:
            return {'message': 'This Movie already exists'}, 400
        movie = Movie(
            name=json_data['name_kr']
        )

        db.session.add(movie)
        db.session.commit()

        result = movie_schema.dump(movie).data

        return {'status': 'success', 'data': result}, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        data, errors = movie_schema.load(json_data)
        if errors:
            return errors, 422
        movie = Movie.query.filter_by(id=data['id']).first()

        if not movie:
            return {'message': 'Movie does not exist'}, 400
        movie.name_kr = data['name_kr']
        db.session.commit()

        result = movie_schema.dump(movie).data

        return {'status': 'success', 'data': result}, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        data, errors = movie_schema.load(json_data)
        if errors:
            return errors, 422
        movie = Movie.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = movie_schema.dump(movie).data

        return {'status': 'success', 'data': result}, 204
