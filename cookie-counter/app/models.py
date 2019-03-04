from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship
from app import db

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
