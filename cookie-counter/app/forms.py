from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DirectorForm(FlaskForm):
    director_kr_name = StringField('Director Korean Name', validators=[DataRequired()])
    director_en_name = StringField('Director English Name', validators=[DataRequired()])
    submit = SubmitField('Register')


class ActorForm(FlaskForm):
    actor_kr_name = StringField('Actor Korean Name', validators=[DataRequired()])
    actor_en_name = StringField('Actor English Name', validators=[DataRequired()])
    submit = SubmitField('Register')