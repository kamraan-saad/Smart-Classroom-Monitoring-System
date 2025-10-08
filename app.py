from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import cv2
import threading
import base64
from modules.attendance import run_attendance
from modules.emotion import run_emotion
# ... import other modules

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)

# User model
class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, email FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return User(user[0], user[1]) if user else None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE email = ?", (data['email'],))
    user = c.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], data['password']):
        login_user(User(user[0], data['email']))
        return jsonify({"success": True})
    return jsonify({"success": False}), 401

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/start_module/<module_id>', methods=['POST'])
@login_required
def start_module(module_id):
    # Start the corresponding Python module in a thread
    if module_id == 'attendance':
        threading.Thread(target=run_attendance, args=(socketio,)).start()
    elif module_id == 'emotion':
        threading.Thread(target=run_emotion, args=(socketio,)).start()
    # ... other modules
    return jsonify({"status": "started"})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)