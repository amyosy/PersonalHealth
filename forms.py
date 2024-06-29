from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class DataForm(FlaskForm):
    blood_pressure = StringField('Blood Pressure', validators=[DataRequired()])
    heart_rate = IntegerField('Heart Rate', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    sleep = IntegerField('Sleep (hours)', validators=[DataRequired()])
    stress = IntegerField('Stress Level (1-10)', validators=[DataRequired()])
    submit = SubmitField('Submit Data')


class GoalForm(FlaskForm):
    goal = StringField('Health Goal', validators=[DataRequired()])
    progress = StringField('Progress', validators=[DataRequired()])
    submit = SubmitField('Set Goal')


class ReminderForm(FlaskForm):
    reminder = StringField('Reminder', validators=[DataRequired()])
    submit = SubmitField('Add Reminder')
