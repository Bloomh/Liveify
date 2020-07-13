from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, widgets
from wtforms.validators import DataRequired

class Input(FlaskForm):
    username = StringField('Name your concert!', validators=[DataRequired()])
    mood = StringField('The general mood of the song', validators=[DataRequired()])
    danceability = StringField('How danceable should the song be?', validators=[DataRequired()])
    energy = StringField('How energetic should the playlist be?', validators=[DataRequired()])
    submit = SubmitField('Click Here to Enter!')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')