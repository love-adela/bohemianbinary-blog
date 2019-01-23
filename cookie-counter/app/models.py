from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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
    directors = relationship("Director", secondary=movie_with_director)
    actors = relationship("Actor", secondary=movie_with_actor)
    image_file_name = Column(String(120))

    def add_movie_to_director(self, movie):
        self.directors.append(movie)

    def add_movie_to_actor(self, movie):
        self.actors.append(movie)

    def __repr__(self):
        return "<Movie('%s', ('%s'))>" % (self.name_en, self.name_kr)


class Cookie(db.Model):
    id = Column(Integer, primary_key=True)
    description_en = Column(String(120))
    description_kr = Column(String(120))
    movie_id = Column(Integer, ForeignKey('movie.id'))
