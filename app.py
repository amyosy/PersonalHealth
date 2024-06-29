from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask.json import jsonify
from forms import RegistrationForm, LoginForm, DataForm, GoalForm, ReminderForm
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# Dummy user data
users = {}

# Dummy health data
health_data = {}

# Dummy goals data
goals_data = {}

# Dummy reminders data
reminders_data = {}

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        if username in users:
            flash('Username already exists.')
        else:
            users[username] = {
                'password': form.password.data
            }
            flash('Registration successful!')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        if username in users and users[username]['password'] == form.password.data:
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('input_data'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/input_data', methods=['GET', 'POST'])
@login_required
def input_data():
    form = DataForm()
    if form.validate_on_submit():
        username = session['username']
        if username not in health_data:
            health_data[username] = []
        health_data[username].append({
            'blood_pressure': form.blood_pressure.data,
            'heart_rate': form.heart_rate.data,
            'weight': form.weight.data,
            'height': form.height.data,
            'sleep': form.sleep.data,
            'stress': form.stress.data
        })
        flash('Data submitted successfully!')
    return render_template('input_data.html', form=form)

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    form = GoalForm()
    if form.validate_on_submit():
        username = session['username']
        if username not in goals_data:
            goals_data[username] = []
        goals_data[username].append({
            'goal': form.goal.data,
            'progress': form.progress.data
        })
        flash('Goal added successfully!')
    return render_template('goals.html', form=form)

@app.route('/reminders', methods=['GET', 'POST'])
@login_required
def reminders():
    form = ReminderForm()
    if form.validate_on_submit():
        username = session['username']
        if username not in reminders_data:
            reminders_data[username] = []
        reminders_data[username].append({
            'reminder': form.reminder.data
        })
        flash('Reminder added successfully!')
    return render_template('reminders.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title='Dashboard')
@app.route('/plots')
@login_required
def plots():
    username = session['username']
    data = health_data.get(username, [])
    return render_template('plots.html', data=jsonify(data))

if __name__ == '__main__':
    app.run(debug=True)
