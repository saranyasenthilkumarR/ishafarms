from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        database='ishafarmsdb'
    )

@app.route('/products', methods=['GET'])
def get_products():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute('SELECT * FROM products WHERE stock_qty > 0')
    return jsonify(cur.fetchall())

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute('SELECT * FROM products WHERE id = %s', (id,))
    return jsonify(cur.fetchone())

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'product-service'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
