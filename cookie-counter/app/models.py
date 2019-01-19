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

actor_association_table = Table('actor_association',
                                db.Model.metadata,
                                Column('movie_id', Integer, ForeignKey('movie.id')),
                                Column('actor_id', Integer, ForeignKey('actor.id'))
                                )


class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    name_en = Column(String(120))
    name_kr = Column(String(120))
    photo = Column(String(120))
    directors = relationship("Director",
                             # primaryjoin=movie_with_director,
                             secondary=movie_with_director,
                             backref=db.backref("movies", lazy='dynamic'))
    image_file_name = Column(String(120))

    def add(self, movie):
        if not self.is_movie(movie):
            self.directors.append(movie)

    def emit(self, movie):
        if self.is_movie(movie):
            self.directors.remove(movie)

    def is_movie(self, movie):
        return self.directors.filter(
            movie.c.director_id == movie.id).count() > 0

    def directors_lists(self):
        director = Director.query.join(
            movie_with_director, (movie_with_director.c.directors_id == Director.movie_id)).filter(
            movie_with_director.c.movie_id == self.id)
        own = Director.query.filter_by(user_id=self.id)
        return director.union(own)

    def __repr__(self):
        return "<Movie('%s', ('%s'))>" % (self.name_en, self.name_kr)


class Director(db.Model):
    id = Column(Integer, primary_key=True)
    name_en = Column(String(120))
    name_kr = Column(String(120))
    photo = Column(String(120))
    movie_id = Column(Integer, ForeignKey('movie.id'))

    def __repr__(self):
        return "<Movie Director('%s', ('%s'))>" % (self.name_en, self.name_kr)
        # TODO: __repr__ 수정 필요 - 무엇을 의미하는지 각각 표시할 것!


class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name_en = Column(String(120))
    name_kr = Column(String(120))
    photo = Column(String(120))

    def __repr__(self):
        return "<Movie Actor('%s', '%s')>" % (self.name_en, self.name_kr)
        # TODO: __repr__ 수정 필요 - 무엇을 의미하는지 각각 표시할 것!


class Cookie(db.Model):
    id = Column(Integer, primary_key=True)
    description_en = Column(String(120))
    description_kr = Column(String(120))
    movie_id = Column(Integer, ForeignKey('movie.id'))
