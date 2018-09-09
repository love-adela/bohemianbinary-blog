from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DirectorForm(FlaskForm):
    directorname = StringField('Director_name', validators=[DataRequired()])
    submit = SubmitField('Register')