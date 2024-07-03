import pytest
from app import app, db
from models import User


# Testfall für die Index-Seite
def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b"Welcome to Personal Health Notion" in response.data


# Hilfsfunktion zur Registrierung eines Benutzers
def register_user(username='testuser', email='test@example.com', password='password'):
    with app.test_client() as client:
        return client.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=password
        ), follow_redirects=True)


# Hilfsfunktion zum Einloggen eines Benutzers
def login_user(username='testuser', password='password'):
    with app.test_client() as client:
        return client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


# Testfall für die Benutzerregistrierung
def test_register():
    response = register_user()
    assert response.status_code == 200
    assert b'Registration successful!' in response.data


# Testfall für die Registrierung eines bereits vorhandenen Benutzers
def test_register_existing_user():
    register_user()
    response = register_user()
    assert response.status_code == 200
    assert b'Username already exists.' in response.data


# Testfall für das Benutzer-Login
def test_login():
    register_user()
    response = login_user()
    assert response.status_code == 200
    assert b'Login successful!' in response.data


# Testfall für das Benutzer-Login mit ungültigen Anmeldeinformationen
def test_login_invalid_credentials():
    register_user()
    response = login_user(password='wrongpassword')
    assert response.status_code == 200
    assert b'Invalid credentials.' in response.data


# Testfall für das Benutzer-Logout
def test_logout():
    register_user()
    login_user()
    with app.test_client() as client:
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'You have been logged out.' in response.data


# Testfall für das Eingeben von Gesundheitsdaten
def test_input_data():
    register_user()
    login_user()
    with app.test_client() as client:
        response = client.post('/input_data', data=dict(
            blood_pressure='120/80',
            heart_rate=70,
            weight=70.5,
            height=175.0,
            sleep='8',
            stress='3'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert b'Data submitted successfully!' in response.data


# Testfall für das Hinzufügen von Erinnerungen
def test_reminders():
    register_user()
    login_user()
    with app.test_client() as client:
        response = client.post('/reminders', data=dict(
            reminder='Take medication at 8 PM'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert b'Reminder added successfully!' in response.data


# Testfall für das Abrufen des Dashboards
def test_dashboard():
    register_user()
    login_user()
    with app.test_client() as client:
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'Your Health Data' in response.data
        assert b'Your Reminders' in response.data


# Testfall für das Abrufen der Plots
def test_plots():
    register_user()
    login_user()
    with app.test_client() as client:
        # Hinzufügen einiger Gesundheitsdaten für das Plotten
        client.post('/input_data', data=dict(
            blood_pressure='120/80',
            heart_rate=70,
            weight=70.5,
            height=175.0,
            sleep='8',
            stress='3'
        ), follow_redirects=True)
        response = client.get('/plots?page=1')
        assert response.status_code == 200
        assert b'Weight Over Time' in response.data
