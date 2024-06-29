# Personal Health Notion

A simple Flask web application to track personal health data, set goals, and add reminders.

## Features

- User Registration and Login
- Input Health Data (Blood Pressure, Heart Rate, Weight, Height, Sleep, Stress)
- Set Health Goals
- Add Reminders
- Visualize Data with Plots

## Setup

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd personal_health_notion
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    python app.py
    ```

5. Run the tests:
    ```sh
    pytest
    ```

## Usage

- Visit `http://127.0.0.1:5000` in your browser to access the application.
- Register a new account or login with an existing account.
- Input your health data, set goals, and add reminders.

## License

This project is licensed under the MIT License.
