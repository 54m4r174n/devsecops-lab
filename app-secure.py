from flask import Flask, request, redirect, jsonify
import sqlite3
import subprocess
import os
import hashlib
import yaml

app = Flask(__name__)

def get_db():
    return sqlite3.connect('users.db')

@app.route('/login')
def login():
    username = request.args.get('username', '')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    return jsonify({"user": str(user)})

@app.route('/ping')
def ping():
    host = request.args.get('host', '')

    if not host.replace('.', '').isalnum():
        return "Invalid host", 400

    try:
        result = subprocess.check_output(
            ['ping', '-c', '1', host],
            stderr=subprocess.STDOUT
        )
        return result
    except subprocess.CalledProcessError:
        return "Ping failed", 500

API_KEY = os.getenv("API_KEY", "default_key")

@app.route('/profile')
def profile():
    data = request.cookies.get('data', '{}')
    return jsonify({"data": data})

@app.route('/read')
def read_file():
    filename = request.args.get('file', '')

    base_path = '/var/app/'
    safe_path = os.path.abspath(os.path.join(base_path, filename))

    if not safe_path.startswith(base_path):
        return "Access denied", 403

    if not os.path.exists(safe_path):
        return "File not found", 404

    with open(safe_path, 'r') as f:
        return f.read()

@app.route('/goto')
def goto():
    url = request.args.get('url', '')

    if not url.startswith('/'):
        return "Invalid redirect", 400

    return redirect(url)

@app.route('/config')
def config():
    data = request.args.get('data', '')

    try:
        parsed = yaml.safe_load(data)
        return jsonify(parsed)
    except:
        return "Invalid YAML", 400

@app.route('/hash')
def secure_hash():
    password = request.args.get('password', '')

    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1')
