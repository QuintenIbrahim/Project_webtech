from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from mijnproject.models import User, Acteur, Film, Regisseur


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
    voornaam = StringField('Voornaam', validators=[DataRequired()])
    achternaam = StringField('Achternaam', validators=[DataRequired()])
    #film = SelectField(label='Film', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    submit = SubmitField('Voeg toe')

    def validate_voornaam(self, field):
        if Acteur.query.filter_by(voornaam=field.data).first():
            raise ValidationError("Deze voornaam is al in gebruik")

    def validate_achternaam(self, field):
        if Acteur.query.filter_by(achternaam=field.data).first():
            raise ValidationError("Deze achternaam is al in gebruik")

class regisseurForm(FlaskForm):
    voornaam = StringField('Voornaam', validators=[DataRequired()])
    achternaam = StringField('Achternaam', validators=[DataRequired()])
    #film = SelectField(label='Film', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    submit = SubmitField('Voeg toe')

    def validate_voornaam(self, field):
        if Regisseur.query.filter_by(voornaam=field.data).first():
            raise ValidationError("Deze voornaam is al in gebruik")

    def validate_achternaam(self, field):
        if Regisseur.query.filter_by(achternaam=field.data).first():
            raise ValidationError("Deze achternaam is al in gebruik")

class filmForm(FlaskForm):
    titel = StringField('Titel', validators=[DataRequired()])
    datum = DateField('Datum', validators=[DataRequired()], format='%Y-%m-%d')
    rating = IntegerField('Rating', validators=[DataRequired()])
    citaten = StringField('Citaten', validators=[DataRequired()])
    img = FileField('Image')
    submit = SubmitField('Voeg toe')

    def validate_titel(self, field):
        if Film.query.filter_by(titel=field.data).first():
            raise ValidationError("Deze titel is al in gebruik")