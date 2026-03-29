from flask import Flask, request, redirect
import sqlite3
import subprocess
import pickle
import base64
import yaml
import hashlib

app = Flask(__name__)

# VULN 1: SQL Injection
@app.route('/login')
def login():
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    query = "SELECT * FROM users WHERE username='" + username + "'"
    conn.execute(query)
    return "Login: " + username

# VULN 2: Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host')
    result = subprocess.check_output('ping -c 1 ' + host, shell=True)
    return result

# VULN 3: Hardcoded Secrets — GitLeaks pakdega
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD = "admin123"
GITHUB_TOKEN = "ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
API_KEY = "sk-proj-abcdefghijklmnop1234567890"

# VULN 4: Pickle Deserialization — RCE possible
@app.route('/profile')
def profile():
    data = request.cookies.get('data')
    obj = pickle.loads(base64.b64decode(data))
    return str(obj)

# VULN 5: Path Traversal
@app.route('/read')
def read_file():
    filename = request.args.get('file')
    filepath = '/var/app/' + filename
    with open(filepath, 'r') as f:
        return f.read()

# VULN 6: Open Redirect
@app.route('/goto')
def goto():
    url = request.args.get('url')
    return redirect(url)

# VULN 7: YAML Deserialization — RCE
@app.route('/config')
def config():
    data = request.args.get('data')
    parsed = yaml.load(data)
    return str(parsed)

# VULN 8: Weak Hashing
@app.route('/hash')
def weak_hash():
    password = request.args.get('password')
    hashed = hashlib.md5(password.encode()).hexdigest()
    return hashed

# VULN 9: Debug Mode ON — information disclosure
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
