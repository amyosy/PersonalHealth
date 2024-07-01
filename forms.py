from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateField, TextAreaField, \
    BooleanField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


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
    sleep = SelectField('Sleep', choices=[(str(i), str(i)) for i in range(1, 13)], validators=[DataRequired()])
    stress = SelectField('Stress', choices=[(str(i), str(i)) for i in range(1, 6)], validators=[DataRequired()])
    submit = SubmitField('Submit Data')


class GoalForm(FlaskForm):
    goal_title = StringField('Goal Title', validators=[DataRequired(), Length(min=2, max=50)])
    goal_description = TextAreaField('Goal Description', validators=[DataRequired()])
    goal_deadline = DateField('Goal Deadline', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Goal')


class ReminderForm(FlaskForm):
    reminder = StringField('Reminder', validators=[DataRequired()])
    submit = SubmitField('Add Reminder')
