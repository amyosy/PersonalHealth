from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DataForm(FlaskForm):
    blood_pressure = StringField('Blood Pressure', validators=[DataRequired()])
    heart_rate = IntegerField('Heart Rate', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    sleep = IntegerField('Sleep', validators=[DataRequired()])
    stress = IntegerField('Stress', validators=[DataRequired()])
    submit = SubmitField('Submit Data')


class GoalForm(FlaskForm):
    goal = StringField('Goal', validators=[DataRequired()])
    progress = StringField('Progress', validators=[DataRequired()])
    submit = SubmitField('Set Goal')


class ReminderForm(FlaskForm):
    reminder = StringField('Reminder', validators=[DataRequired()])
    submit = SubmitField('Set Reminder')


class ReminderForm(FlaskForm):
    reminder = StringField('Reminder', validators=[DataRequired()])
    submit = SubmitField('Add Reminder')
