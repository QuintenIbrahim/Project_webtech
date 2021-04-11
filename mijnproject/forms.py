from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from mijnproject.models import User, Acteur, film


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if not user or not user.check_password(field.data):
            raise ValidationError('Login not successful')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Registreer!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("E-mail already taken")

    def validate_password(self, field):
        if len(field.data) < 3:
            raise ValidationError("Password too short")


class acteurForm(FlaskForm):
    voornaam = StringField('voornaam', validators=[DataRequired()])
    achternaam = StringField('achternaam', validators=[DataRequired()])
    submit = SubmitField('Voeg toe')

class filmForm(FlaskForm):
    titel = StringField('Titel', validators=[DataRequired()])
    datum = IntegerField('Datum', validators=[DataRequired()])
    submit = SubmitField('Voeg toe')

