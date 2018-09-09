from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy import Column, Integer, String
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship
from app import db

engine = create_engine('sqlite:///memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def create_db():
    Base.metadata.create_all(engine)


director_association_table = Table(
    'director_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('director_id', Integer, ForeignKey('director.id'))
)

actor_associtation_table = Table(
    'actor_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('actor_id', Integer, ForeignKey('actor.id'))
)


class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    name_en = Column(String(120), primary_key=True)
    name_kr = Column(String(120))
    directors = relationship("Director",
                             secondary=director_association_table,
                             backref="movies")
    actors = relationship("Actor",
                          secondary=actor_associtation_table,
                          backref="movies")
    cookies = relationship("Cookie", backref="movie")
    image_file_name = Column(String(120))

    def __repr__(self):
        return "<Movie('%s', '%s')> % (self.name_en, self.name_kr)"
        # TODO: __repr__ 수정 필요 - 무엇을 의미하는지 각각 표시할 것!


class Director(db.Model):
    id = Column(Integer, primary_key=True)
    name_en = Column(String(120), primary_key=True)
    name_kr = Column(String(120))

    def __repr__(self):
        return "<Movie Director('%s', '%s')> % (self.name_en, self.name_kr)"
        # TODO: __repr__ 수정 필요 - 무엇을 의미하는지 각각 표시할 것!


class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name_en = Column(String(120), primary_key=True)
    name_kr = Column(String(120))

    def __repr__(self):
        return "<Movie Actor('%s', '%s')> % (self.name_en, self.name_kr)"
        # TODO: __repr__ 수정 필요 - 무엇을 의미하는지 각각 표시할 것!


class Cookie(db.Model):
    id = Column(Integer, primary_key=True)
    description_en = Column(String(120))
    description_kr = Column(String(120))


def commit():
    session.commit()
