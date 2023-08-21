from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms import validators


class LoginForm(FlaskForm):
    id = StringField('ID', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Login')


class VoterLoginForm(FlaskForm):
    id = StringField('ID', [validators.InputRequired()])
    submit = SubmitField('Login')
