from flask import Flask, request
import sqlite3
import subprocess
import pickle
import base64

app = Flask(__name__)

# VULN 1: SQL Injection
@app.route('/login')
def login():
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    query = "SELECT * FROM users WHERE username='" + username + "'"
#    conn.execute(query)
#    return "Login: " + username
    cursor = conn.execute(query)
    data = cursor.fetchall()
    return str(data)

# VULN 2: Command Injection  
@app.route('/ping')
def ping():
    host = request.args.get('host')
    result = subprocess.check_output('ping -c 1 ' + host, shell=True)
    return result

# VULN 3: Hardcoded Secret
AWS_SECRET = "AKIAIOSFODNN7EXAMPLE"
DB_PASSWORD = "admin123"

# VULN 4: Pickle Deserialization
@app.route('/profile')
def profile():
    data = request.cookies.get('data')
    obj = pickle.loads(base64.b64decode(data))
    return str(obj)

if __name__ == '__main__':
    app.run(debug=True)
EOF

