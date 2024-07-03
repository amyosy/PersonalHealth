from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os

# Initialisieren der SQLAlchemy-Datenbankinstanz
db = SQLAlchemy()
# Initialisieren der Bcrypt-Instanz für Passwort-Hashing
bcrypt = Bcrypt()


# Funktion zur Erstellung der Flask-Anwendung
def create_app():
    # Erstellen der Flask-Anwendung
    app = Flask(__name__)
    # Konfiguration des geheimen Schlüssels für die Sitzungsverwaltung
    app.config['SECRET_KEY'] = 'supersecretkey'
    # Konfiguration der Datenbank-URI; verwendet die Umgebungsvariable 'DATABASE_URL' oder eine SQLite-Datenbank als Fallback
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')

    # Initialisieren der Datenbankinstanz mit der Flask-Anwendung
    db.init_app(app)
    # Initialisieren der Bcrypt-Instanz mit der Flask-Anwendung
    bcrypt.init_app(app)
    # Initialisieren der Migrate-Instanz mit der Flask-Anwendung und der Datenbankinstanz
    migrate = Migrate(app, db)

    # Anwendungs-Kontext für die Initialisierung des Schemas und Importieren der Formulare und Modelle
    with app.app_context():
        from forms import RegistrationForm, LoginForm, DataForm, ReminderForm
        from models import User, HealthData, Reminder
        # Erstellen aller Datenbanktabellen basierend auf den Modellen
        db.create_all()

    # Rückgabe der erstellten Flask-Anwendung
    return app
