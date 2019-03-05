from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from app.models import Admin


class DirectorForm(FlaskForm):
    director_kr_name = StringField('Director Korean Name', validators=[DataRequired()])
    director_en_name = StringField('Director English Name', validators=[DataRequired()])
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    delete = SubmitField('Delete')
    submit = SubmitField('Register')


class ActorForm(FlaskForm):
    actor_kr_name = StringField('Actor Korean Name', validators=[DataRequired()])
    actor_en_name = StringField('Actor English Name', validators=[DataRequired()])
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    delete = SubmitField('Delete')
    submit = SubmitField('Register')


class MovieForm(FlaskForm):
    movie_kr_name = StringField('Movie Korean Name', validators=[DataRequired()])
    movie_en_name = StringField('Movie English Name', validators=[DataRequired()])
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'gif'], 'Images only!')
    ])
    delete = SubmitField('Delete')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, name):
        admin = Admin.query.filter_by(name=name.data).first()
        if admin is not None:
            raise ValidationError('Please use a different admin name.')

    def validate_email(self, email):
        admin_user = Admin.query.filter_by(email=email.data).first()
        if admin_user is not None:
            raise ValidationError('Please use a different email address.')
