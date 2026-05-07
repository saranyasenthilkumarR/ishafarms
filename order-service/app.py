from flask import Flask, jsonify, request
import mysql.connector
import os
import requests

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        database='ishafarmsdb'
    )

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.json
    product_url = os.environ['PRODUCT_SERVICE_URL']
    product = requests.get(f"{product_url}/products/{data['product_id']}").json()
    total = product['price'] * data['quantity']
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'INSERT INTO orders (user_id, product_id, quantity, total_price, delivery_address) VALUES (%s, %s, %s, %s, %s)',
        (data['user_id'], data['product_id'], data['quantity'], total, data['delivery_address'])
    )
    db.commit()
    return jsonify({'message': 'Order placed!', 'total': float(total)}), 201

@app.route('/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute('SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC', (user_id,))
    return jsonify(cur.fetchall())

@app.route('/orders/status/<int:order_id>', methods=['GET'])
def order_status(order_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute('SELECT id, status, total_price, created_at FROM orders WHERE id = %s', (order_id,))
    return jsonify(cur.fetchone())

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'order-service'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003, debug=True)
