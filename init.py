from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os

# Initialisieren der SQLAlchemy-Datenbankinstanz
db = SQLAlchemy()
bcrypt = Bcrypt()  # Initialisieren der Bcrypt-Instanz für Passwort-Hashing


# Funktion zur Erstellung der Flask-Anwendung
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')

    # Initialisieren der Datenbankinstanz mit der Flask-Anwendung
    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    # Anwendungs-Kontext für die Initialisierung und Importieren der Formulare und Modelle
    with app.app_context():
        from forms import RegistrationForm, LoginForm, DataForm, ReminderForm
        from models import User, HealthData, Reminder
        db.create_all()  # Erstellen aller Datenbanktabellen basierend auf den Modellen

    return app
