from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask.json import jsonify
from forms import RegistrationForm, LoginForm, DataForm, GoalForm, ReminderForm
from functools import wraps
from init import create_app, db, bcrypt
from models import User, HealthData, Goal, Reminder

app = create_app()


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
        # Passwort-Hashing
        username = form.username.data
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # Erstellen eines neuen Benutzers mit dem gehashten Passwort
            user = User(username=username, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['logged_in'] = True
            session['username'] = user.username
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
        user = User.query.filter_by(username=session['username']).first()
        health_data = HealthData(
            blood_pressure=form.blood_pressure.data,
            heart_rate=form.heart_rate.data,
            weight=form.weight.data,
            height=form.height.data,
            sleep=form.sleep.data,
            stress=form.stress.data,
            user_id=user.id
        )
        db.session.add(health_data)
        db.session.commit()
        flash('Data submitted successfully!')
    return render_template('input_data.html', form=form)


@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    form = GoalForm()
    user = User.query.filter_by(username=session['username']).first()
    if form.validate_on_submit():
        goal = Goal(title=form.goal_title.data, description=form.goal_description.data,
                    deadline=form.goal_deadline.data, user_id=user.id)
        db.session.add(goal)
        db.session.commit()
        flash('Goal added successfully!')
        return redirect(url_for('goals'))
    user_goals = Goal.query.filter_by(user_id=user.id).all()
    return render_template('goals.html', form=form, goals=user_goals)


@app.route('/reminders', methods=['GET', 'POST'])
@login_required
def reminders():
    form = ReminderForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
        reminder = Reminder(reminder=form.reminder.data, user_id=user.id)
        db.session.add(reminder)
        db.session.commit()
        flash('Reminder added successfully!')
    user = User.query.filter_by(username=session['username']).first()
    user_reminders = Reminder.query.filter_by(user_id=user.id).all()
    return render_template('reminders.html', form=form, reminders=user_reminders)


@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(username=session['username']).first()
    health_data = HealthData.query.filter_by(user_id=user.id).all()
    user_goals = Goal.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', health_data=health_data, goals=user_goals, username=user.username)


@app.route('/plots')
@login_required
def plots():
    user = User.query.filter_by(username=session['username']).first()
    data = HealthData.query.filter_by(user_id=user.id).all()
    return render_template('plots.html', data=jsonify(data))


if __name__ == '__main__':
    app.run(debug=True)
