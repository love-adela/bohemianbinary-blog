from app import db

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    director_name_en = db.Column(db.String(64), index=True, unique=True)
    director_name_kr = db.Column(db.String(50), index=True, unique=True)

    def __repr__(self):
        return '<Director {} , {}>'.format(self.director_name_en, self.director_name_kr)


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_name_en = db.Column(db.String(64), index=True, unique=True)
    actor_name_kr = db.Column(db.String(50), index=True, unique=True)

    def __repr__(self):
        return '<Actor {} , {}>'.format(self.actor_name_en, self.actor_name_kr)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_name_en = db.Column(db.String(120), index=True, unique=True)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))

    def __repr__(self):
        return '<Movie {}>'.format(self.movie_name_en, self.director_id, self.actor_id)