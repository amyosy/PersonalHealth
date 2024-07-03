from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')

    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from forms import RegistrationForm, LoginForm, DataForm, ReminderForm
        from models import User, HealthData, Reminder
        db.create_all()

    return app
