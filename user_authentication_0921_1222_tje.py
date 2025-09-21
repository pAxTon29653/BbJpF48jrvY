# 代码生成时间: 2025-09-21 12:22:41
from celery import Celery
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize the Flask application
app = Flask(__name__)

# Configuration for Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# User database (for demonstration purposes, use a real database in production)
users = {}

# Authenticate user
def authenticate_user(username, password):
    """
    Authenticate a user by checking the username and password against the stored credentials.
    Returns True if authentication is successful, False otherwise.
    """
    # Check if the user exists and the password is correct
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        return True
    else:
        return False

# Celery task to handle user authentication
@celery.task(name='authenticate_user_task')
def authenticate_user_task(username, password):
    """
    Celery task to authenticate user asynchronously.
    """
    return authenticate_user(username, password)

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint to handle user login.
    It expects a JSON payload with 'username' and 'password'.
    Returns a JSON with authentication status and user information if successful.
    """
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    # Use Celery task to handle authentication asynchronously
    result = authenticate_user_task.apply_async((username, password))
    
    # Wait for the result (in a real-world scenario, you would not block the request)
    # For demonstration purposes, we wait for the result to be ready
    result.get()
    
    # Get the result of the authentication
    auth_status = result.get()
    if auth_status:
        user_info = users.get(username, {})
        return jsonify({'status': 'success', 'user': user_info}), 200
    else:
        return jsonify({'status': 'failed', 'error': 'Invalid credentials'}), 401

# Register a user (for demonstration purposes)
@app.route('/register', methods=['POST'])
def register():
    """
    Endpoint to handle user registration.
    It expects a JSON payload with 'username' and 'password'.
    Returns a JSON with registration status.
    """
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']
    hashed_password = generate_password_hash(password)

    if username in users:
        return jsonify({'status': 'failed', 'error': 'User already exists'}), 409
    else:
        users[username] = {'password': hashed_password}
        return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)