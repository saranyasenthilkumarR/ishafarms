from flask import Flask, jsonify, request
import mysql.connector
import os
import jwt
import bcrypt
from datetime import datetime, timedelta

app = Flask(__name__)
SECRET_KEY = "ishafarms-secret-key"

def get_db():
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        database='ishafarmsdb'
    )

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'INSERT INTO users (name, email, password_hash, phone) VALUES (%s, %s, %s, %s)',
        (data['name'], data['email'], hashed.decode(), data.get('phone',''))
    )
    db.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute('SELECT * FROM users WHERE email = %s', (data['email'],))
    user = cur.fetchone()
    if user and bcrypt.checkpw(data['password'].encode(), user['password_hash'].encode()):
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token, 'name': user['name']})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute('SELECT id, name, email, phone, address FROM users WHERE id = %s', (user_id,))
    return jsonify(cur.fetchone())

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'user-service'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)
