from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


# Registrierungsformular
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


# Loginformular
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# Datenformular
class DataForm(FlaskForm):
    blood_pressure = StringField('Blood Pressure', validators=[DataRequired()])
    heart_rate = IntegerField('Heart Rate', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    sleep = SelectField('Sleep', choices=[(str(i), str(i)) for i in range(1, 13)], validators=[DataRequired()])
    stress = SelectField('Stress', choices=[(str(i), str(i)) for i in range(1, 6)], validators=[DataRequired()])
    submit = SubmitField('Submit Data')


# Formular für die Plot-Pagination
class PlotPaginationForm(FlaskForm):
    weight_submit = SubmitField('Weight')
    height_submit = SubmitField('Height')
    heart_rate_submit = SubmitField('Heart Rate')
    blood_pressure_submit = SubmitField('Blood Pressure')
    sleep_submit = SubmitField('Sleep')
    stress_submit = SubmitField('Stress')


# Erinnerungsformular
class ReminderForm(FlaskForm):
    reminder = StringField('Reminder', validators=[DataRequired()])
    submit = SubmitField('Add Reminder')
