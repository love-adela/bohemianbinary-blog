from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DirectorForm(FlaskForm):
    director_kr_name = StringField('Director Korean Name', validators=[DataRequired()])
    director_en_name = StringField('Director English Name', validators=[DataRequired()])
    photo = FileField('Photo', validators=[
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Register')


class ActorForm(FlaskForm):
    actor_kr_name = StringField('Actor Korean Name', validators=[DataRequired()])
    actor_en_name = StringField('Actor English Name', validators=[DataRequired()])
    photo = FileField('Photo', validators=[
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    delete = SubmitField('Delete')
    submit = SubmitField('Register')


class MovieForm(FlaskForm):
    movie_kr_name = StringField('Movie Korean Name', validators=[DataRequired()])
    movie_en_name = StringField('Movie English Name', validators=[DataRequired()])
    photo = FileField('Photo', validators=[
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    delete = SubmitField('Delete')
    submit = SubmitField('Register')
