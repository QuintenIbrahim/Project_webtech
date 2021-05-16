import base64

from mijnproject import app, db
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user
from mijnproject.models import User, Acteur, Regisseur, Film, rol
from mijnproject.forms import LoginForm, RegistrationForm, acteurForm, filmForm, regisseurForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def home():
    films = Film.query.all()
    film = Film.query.filter_by().first()
    image = base64.b64encode(film.img).decode('ascii')
    return render_template('home.html', films=films, data=list, image=image)



@app.route('/welkom')
@login_required
def welkom():
    return render_template('welkom.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('home'))

@app.route('/acteur_toevoegen', methods=['GET', 'POST'])
@login_required
def acteur_toevoegen():
    Acteurform = acteurForm()
    Regisseurform = regisseurForm()
    Filmform = filmForm()
    if Acteurform.validate_on_submit():
        # Voeg een nieuwe acteur toe aan de database
        new_acteur = Acteur(Acteurform.voornaam.data,
                          Acteurform.achternaam.data)
        db.session.add(new_acteur)
        db.session.commit()
        flash('De acteur is succesvol toegevoegd!')
        return redirect(url_for('films'))

    if Regisseurform.validate_on_submit():
        # Voeg een nieuwe regisseur toe aan de database
        new_regisseur = Regisseur(Regisseurform.voornaam.data,
                            Regisseurform.achternaam.data)
        db.session.add(new_regisseur)
        db.session.commit()
        flash('De regisseur is succesvol toegevoegd!')
        return redirect(url_for('films'))

    if Filmform.validate_on_submit():
        # Voeg een nieuwe film toe aan de database
        img = request.files['img']
        filename = secure_filename(img.filename)
        new_film = Film(Filmform.titel.data,
                        Filmform.datum.data,
                        Filmform.rating.data,
                        Filmform.citaten.data,
                        img=img.read(),
                        name=filename)
        db.session.add(new_film)
        db.session.commit()
        flash('De film is succesvol toegevoegd!')
        return redirect(url_for('films'))

    return render_template('acteur_toevoegen.html', Aform=Acteurform, Rform=Regisseurform, Fform=Filmform)


@app.route('/films')
def films():
    films = Film.query.all()
    file_data = Film.query.filter_by().first()
    image = base64.b64encode(file_data.img).decode('ascii')
    return render_template('films.html', films=films, data=list, image=image)


@app.route('/film_pagina')
def film_pagina():
    film = Film.query.all()
    return render_template('film_pagina.html', film=film)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            # Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0] == '/':
                next = url_for('welkom')

            return redirect(next)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden! ')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)
