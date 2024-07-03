from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


# Definition des Registrierungsformulars
class RegistrationForm(FlaskForm):
    # Benutzername-Feld mit DataRequired und Length Validierung
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # E-Mail-Feld mit DataRequired und Email Validierung
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Passwort-Feld mit DataRequired Validierung
    password = PasswordField('Password', validators=[DataRequired()])
    # Passwortbestätigungs-Feld mit DataRequired und EqualTo Validierung
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Senden-Button
    submit = SubmitField('Sign Up')


# Definition des Login-Formulars
class LoginForm(FlaskForm):
    # Benutzername-Feld mit DataRequired und Length Validierung
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # Passwort-Feld mit DataRequired Validierung
    password = PasswordField('Password', validators=[DataRequired()])
    # Erinnerung-Checkbox
    remember = BooleanField('Remember Me')
    # Senden-Button
    submit = SubmitField('Login')


# Definition des Formulars für Gesundheitsdaten
class DataForm(FlaskForm):
    # Blutdruck-Feld mit DataRequired Validierung
    blood_pressure = StringField('Blood Pressure', validators=[DataRequired()])
    # Herzfrequenz-Feld mit DataRequired Validierung
    heart_rate = IntegerField('Heart Rate', validators=[DataRequired()])
    # Gewicht-Feld mit DataRequired Validierung
    weight = FloatField('Weight', validators=[DataRequired()])
    # Größe-Feld mit DataRequired Validierung
    height = FloatField('Height', validators=[DataRequired()])
    # Schlaf-Feld mit DataRequired Validierung und Auswahlmöglichkeiten von 1 bis 12
    sleep = SelectField('Sleep', choices=[(str(i), str(i)) for i in range(1, 13)], validators=[DataRequired()])
    # Stress-Feld mit DataRequired Validierung und Auswahlmöglichkeiten von 1 bis 5
    stress = SelectField('Stress', choices=[(str(i), str(i)) for i in range(1, 6)], validators=[DataRequired()])
    # Senden-Button
    submit = SubmitField('Submit Data')


# Formular für die Plot-Pagination
class PlotPaginationForm(FlaskForm):
    # Button für Gewicht-Plot
    weight_submit = SubmitField('Weight')
    # Button für Größen-Plot
    height_submit = SubmitField('Height')
    # Button für Herzfrequenz-Plot
    heart_rate_submit = SubmitField('Heart Rate')
    # Button für Blutdruck-Plot
    blood_pressure_submit = SubmitField('Blood Pressure')
    # Button für Schlaf-Plot
    sleep_submit = SubmitField('Sleep')
    # Button für Stress-Plot
    stress_submit = SubmitField('Stress')


# Definition des Formulars für Erinnerungen
class ReminderForm(FlaskForm):
    # Erinnerungs-Feld mit DataRequired Validierung
    reminder = StringField('Reminder', validators=[DataRequired()])
    # Senden-Button
    submit = SubmitField('Add Reminder')
