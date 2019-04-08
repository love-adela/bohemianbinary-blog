from flask import jsonify, request
from flask_restful import Resource
from app.models import db, Movie, Director, DirectorSchema

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()


class DirectorResource(Resource):
    def get(self):
        directors = Director.query.all()
        directors = directors_schema.dump(directors).data
        return {'status': 'success', 'data': directors}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        data, errors = director_schema.load(json_data)
        if errors:
            return {'status': 'error', 'data': errors}, 422
        movie_id = Movie.query.filter_by(id=data['movie_id']).first()
        if not movie_id:
            return {'status': 'error', 'message': 'Director for this movie not found.'}
        director = Director(
            movie_id=data['movie_id'],
            director=data['director']
        )
        db.session.add(director)
        db.session.commit()

        result = director_schema.dump(director).data

        return {'status': 'success', 'data': result}, 201

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        data, errors = director_schema.load(json_data)
        if errors:
            return errors, 422
        director = Director.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = director_schema.dump(director).data

        return {'status': 'success', 'data': result}, 204

