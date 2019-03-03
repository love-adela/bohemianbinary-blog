from flask import Flask
from config import Config
import json

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return {x.name: getattr(obj, x.name) for x in obj.__table__.columns}
        else:
            json.JSONEncoder.default(self, obj)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.admin import bp as admin_bp

    app.register_blueprint(admin_bp, url_prefix='/bb-admin')
    app.json_encoder = Encoder

    return app

from app import models