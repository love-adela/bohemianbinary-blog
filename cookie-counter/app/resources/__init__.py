from flask import Blueprint
from flask_restful import Api
from resources.Movie import MovieResource
from resources.Director import DirectorResource
from resources.Actor import ActorResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(MovieResource, '/Movie')
api.add_resource(DirectorResource, '/Director')
api.add_resource(ActorResource, '/Actor')
