# Importieren der notwendigen Module
import io
from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField
from forms import RegistrationForm, LoginForm, DataForm, ReminderForm, PlotPaginationForm
from functools import wraps
from init import create_app, db, bcrypt
from models import User, HealthData, Reminder
import matplotlib.pyplot as plt
import base64

# Erstellen der Flask-App mit den Konfigurationen aus create_app()
app = create_app()


# Dekorator, um sicherzustellen, dass bestimmte Routen nur von eingeloggten Benutzern aufgerufen werden können
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))

    return wrap


# Route für die Startseite der Anwendung
@app.route('/')
def index():
    return render_template('index.html')


# Route für die Registrierung neuer Benutzer
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        # Überprüfen, ob der Benutzername bereits existiert
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
        else:
            # Hashen des Passworts
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # Erstellen eines neuen Benutzers mit dem gehashten Passwort
            user = User(username=username, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Route für das Login der Benutzer
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Überprüfen der Benutzerdaten und des Passworts
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['logged_in'] = True
            session['username'] = user.username
            flash('Login successful!')
            return redirect(url_for('input_data'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html', form=form)


# Route für das Logout der Benutzer
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))


# Route für die Eingabe von Gesundheitsdaten
@app.route('/input_data', methods=['GET', 'POST'])
@login_required
def input_data():
    form = DataForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
        # Erstellen eines neuen HealthData-Datensatzes
        health_data = HealthData(
            blood_pressure=form.blood_pressure.data,
            heart_rate=form.heart_rate.data,
            weight=form.weight.data,
            height=form.height.data,
            sleep=form.sleep.data,
            stress=form.stress.data,
            user_id=user.id
        )
        db.session.add(health_data)
        db.session.commit()
        flash('Data submitted successfully!')
    return render_template('input_data.html', form=form)


# Route für die Verwaltung von Erinnerungen
@app.route('/reminders', methods=['GET', 'POST'])
@login_required
def reminders():
    form = ReminderForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
        # Erstellen eines neuen Reminder-Datensatzes
        reminder = Reminder(reminder=form.reminder.data, user_id=user.id)
        db.session.add(reminder)
        db.session.commit()
        flash('Reminder added successfully!')
    user = User.query.filter_by(username=session['username']).first()
    user_reminders = Reminder.query.filter_by(user_id=user.id).all()
    return render_template('reminders.html', form=form, reminders=user_reminders)


# Route für das Dashboard, das Gesundheitsdaten und Erinnerungen anzeigt
@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(username=session['username']).first()
    health_data = HealthData.query.filter_by(user_id=user.id).all()
    reminders = Reminder.query.filter_by(user_id=user.id).all()  # Fetch reminders
    return render_template('dashboard.html', health_data=health_data, reminders=reminders)


# Route für die Erstellung und Anzeige von Plots der Gesundheitsdaten
@app.route('/plots', methods=['GET', 'POST'])
def plots():
    form = PlotPaginationForm()

    # Aktuelle Seite für die Pagination bestimmen
    page = int(request.args.get('page', 1))

    # Abrufen der Daten für die Plots basierend auf der aktuellen Seite
    if page == 1:
        health_data = HealthData.query.with_entities(HealthData.weight).all()
        plot_title = 'Weight Over Time'
    elif page == 2:
        health_data = HealthData.query.with_entities(HealthData.height).all()
        plot_title = 'Height Over Time'
    elif page == 3:
        health_data = HealthData.query.with_entities(HealthData.heart_rate).all()
        plot_title = 'Heart Rate Over Time'
    elif page == 4:
        health_data = HealthData.query.with_entities(HealthData.blood_pressure).all()
        plot_title = 'Blood Pressure Over Time'
    elif page == 5:
        health_data = HealthData.query.with_entities(HealthData.sleep).all()
        plot_title = 'Sleep Over Time'
    elif page == 6:
        health_data = HealthData.query.with_entities(HealthData.stress).all()
        plot_title = 'Stress Over Time'
    else:
        return render_template('error.html', message='Invalid pagination.')

    # Konvertieren der Abfrageergebnisse in eine flache Liste
    health_data = [value[0] for value in health_data]

    # Überprüfen, ob genügend Daten vorhanden sind, um Plots zu erstellen
    if len(health_data) < 3:
        plots_available = False
    else:
        plots_available = True

    if plots_available:
        # Erstellen des Plots
        plt.figure(figsize=(8, 6))
        plt.plot(health_data)
        plt.title(plot_title)
        plt.xlabel('Time')
        plt.ylabel(plot_title)

        # Speichern des Plots in BytesIO
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return render_template('plots.html', form=form, plot_title=plot_title, plot_url=plot_url,
                               plot_available=plots_available, page=page)


# Starten der Flask-Anwendung im Debug-Modus
if __name__ == '__main__':
    app.run(debug=True)
