from flask import Flask

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
import json

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'admin.login'
login.login_message = 'Please log in to access this page.'


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return {x.name: getattr(obj, x.name) for x in obj.__table__.columns}
        else:
            json.JSONEncoder.default(self, obj)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    app.json_encoder = Encoder

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/bb-admin')
    # from app.resources import bp as android_bp
    # app.register_blueprint(android_bp, url_prefix='/bb-resources')

    return app


from app import models
