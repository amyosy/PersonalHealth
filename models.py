from init import db


# Definition des User-Modells
class User(db.Model):
    # Definition der Tabellenfelder und deren Eigenschaften
    id = db.Column(db.Integer, primary_key=True)  # Primärschlüssel
    username = db.Column(db.String(20), unique=True, nullable=False)  # Eindeutiger Benutzername, darf nicht leer sein
    email = db.Column(db.String(120), unique=True, nullable=False)  # Eindeutige E-Mail-Adresse, //
    password = db.Column(db.String(60), nullable=False)  # Passwort-Hash, //
    # Beziehungen zu anderen Tabellen
    health_data = db.relationship('HealthData', backref='author', lazy=True)  # Beziehung zu HealthData
    reminders = db.relationship('Reminder', backref='author', lazy=True)  # Beziehung zu Reminder


# Definition des HealthData-Modells
class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_pressure = db.Column(db.String(20), nullable=False)  # //
    heart_rate = db.Column(db.Integer, nullable=False)  # //
    weight = db.Column(db.Float, nullable=False)  # //
    height = db.Column(db.Float, nullable=False)  # //
    sleep = db.Column(db.Integer, nullable=False)  # //
    stress = db.Column(db.Integer, nullable=False)  # //
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)  # Fremdschlüssel zur User-Tabelle, //


# Definition des Reminder-Modells
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reminder = db.Column(db.String(200), nullable=False)  # Erinnerungstext, //
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)  # Fremdschlüssel zur User-Tabelle, //
