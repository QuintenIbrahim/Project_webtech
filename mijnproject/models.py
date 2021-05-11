from sqlalchemy import UniqueConstraint

from mijnproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# De user_loader decorator zorgt voor de flask-login voor de huidige gebruiker
# en haalt zijn/haar id op.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    # Maak een tabel aan in de database
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Acteur(db.Model):
    # Maak een tabel aan in de database
    __tablename__ = 'Acteur'
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(64), unique=True, index=True)
    achternaam = db.Column(db.String(64), unique=True, index=True)
    rol = db.relationship('rol', backref=db.backref('acteur', lazy=True))
    def __init__(self, voornaam, achternaam):
        self.voornaam = voornaam
        self.achternaam = achternaam

class Regisseur(db.Model):
    # Maak een tabel aan in de database
    __tablename__ = 'Regisseur'
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(64), unique=True, index=True)
    achternaam = db.Column(db.String(64), unique=True, index=True)
    def __init__(self, voornaam, achternaam):
        self.voornaam = voornaam
        self.achternaam = achternaam

class Film(db.Model):
    # Maak een tabel aan in de database
    __tablename__ = 'Film'
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(64), index=True)
    datum = db.Column(db.Date)
    rating = db.Column(db.Integer)
    citaten = db.Column(db.String, index=True)
    rol = db.relationship('rol', backref=db.backref('film', lazy=True))

    def __init__(self, titel, datum, rating, citaten):
        self.titel = titel
        self.datum = datum
        self.rating = rating
        self.citaten = citaten



class rol(db.Model):
    # Maak een tabel aan in de database
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('Film.id'))
    acteur_id = db.Column(db.Integer, db.ForeignKey('Acteur.id'))
    personage = db.Column(db.String)




db.create_all()
