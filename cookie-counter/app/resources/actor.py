from flask import jsonify, request
from flask_restful import Resource
from app.models import db, Movie, Actor, ActorSchema

actors_schema = ActorSchema(many=True)
actor_schema = ActorSchema()


class ActorResource(Resource):
    def get(self):
        actors = Actor.query.all()
        actors = actors_schema.dump(actors).data
        return {'status': 'success', 'data': actors}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        data, errors = actor_schema.load(json_data)
        if errors:
            return {'status': 'error', 'data': errors}, 422
        movie_id = Movie.query.filter_by(id=data['movie_id']).first()
        if not movie_id:
            return {'status': 'error', 'message': 'Actor for this movie not found.'}
        actor = Actor(
            movie_id=data['movie_id'],
            actor=data['actor']
        )
        db.session.add(actor)
        db.session.commit()

        result = actor_schema.dump(actor).data

        return {'status': 'success', 'data': result}, 201

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        data, errors = actor_schema.load(json_data)
        if errors:
            return errors, 422
        actor = Actor.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = actor_schema.dump(actor).data

        return {'status': 'success', 'data': result}, 204

