from flask_marshmallow import Marshmallow

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy import Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask_login import UserMixin

from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from app import db

engine = create_engine('sqlite:///memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def create_db():
    Base.metadata.create_all(engine)


movie_with_director = Table('movie_with_director',
                            db.Model.metadata,
                            Column('movie_id', Integer, ForeignKey('movie.id')),
                            Column('director_id', Integer, ForeignKey('director.id'))
                            )

movie_with_actor = Table('movie_with_actor',
                         db.Model.metadata,
                         Column('movie_id', Integer, ForeignKey('movie.id')),
                         Column('actor_id', Integer, ForeignKey('actor.id'))
                         )


class Director(db.Model):
    id = Column(Integer, primary_key=True)
    name_en = Column(String(120))
    name_kr = Column(String(120))
    photo = Column(String(120))

    def __repr__(self):
        return "<Movie Director('%s', ('%s'))>" % (self.name_en, self.name_kr)


class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name_en = Column(String(120))
    name_kr = Column(String(120))
    photo = Column(String(120))

    def __repr__(self):
        return "<Movie Actor('%s', '%s')>" % (self.name_en, self.name_kr)


class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    name_en = Column(String(120))
    name_kr = Column(String(120))
    photo = Column(String(120))
    number_of_cookies = Column(BigInteger)
    directors = relationship("Director", secondary=movie_with_director)
    actors = relationship("Actor", secondary=movie_with_actor)

    def __repr__(self):
        return "<Movie('%s', ('%s'))>" % (self.name_en, self.name_kr)


class Admin(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<Admin {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))
