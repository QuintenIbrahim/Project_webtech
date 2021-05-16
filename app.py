from mijnproject import app, db
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from mijnproject.models import User, Acteur, Regisseur, Film, rol, Citaten
from mijnproject.forms import LoginForm, RegistrationForm, acteurForm, filmForm, regisseurForm, CitaatForm
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def home():
    films = Film.query.all()
    return render_template('home.html', films=films)



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
        new_film = Film(Filmform.titel.data,
                        Filmform.datum.data,
                        Filmform.rating.data)
        db.session.add(new_film)
        db.session.commit()
        flash('De film is succesvol toegevoegd!')
        return redirect(url_for('films'))

    return render_template('acteur_toevoegen.html', Aform=Acteurform, Rform=Regisseurform, Fform=Filmform, data=Filmform)


@app.route('/films')
def films():
    films = Film.query.all()
    return render_template('films.html', films=films)


@app.route('/film_pagina', methods=['GET', 'POST'])
@login_required
def film_pagina():
    id = request.args.get("filmId")
    citaatForm = CitaatForm()
    if citaatForm.validate_on_submit():
        # Voeg een nieuwe citaat toe aan de database
        new_citaat = Citaten(current_user.username, date.today(), citaatForm.citaten.data, id)
        db.session.add(new_citaat)
        db.session.commit()
        flash('Uw citaat is succesvol toegevoegd!')
        return redirect('film_pagina?filmId='+id)
    film = Film.query.filter(Film.id == id).all()
    citaat = Citaten.query.filter(Citaten.film_id == id).order_by(Citaten.datum.desc()).all()
    return render_template('film_pagina.html', Cform=citaatForm, film=film, citaat=citaat)

@app.route('/film_wijzigen')
def film_wijzigen():
    id = request.args.get("filmId")
    films = Film.query.filter(Film.id == id).all()
    return render_template('film_wijzigen.html', films=films)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Logged in successfully.')
            next = request.args.get('next')
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
