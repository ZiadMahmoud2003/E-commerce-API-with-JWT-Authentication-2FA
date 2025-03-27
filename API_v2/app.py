from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
import pyotp
import qrcode
import io
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ecommerce'
app.config['SECRET_KEY'] = 'ziad'
db = SQLAlchemy(app)
SECRET_KEY = app.config['SECRET_KEY']

# Database Models
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    twofa_secret = db.Column(db.String(256), nullable=False)

class Products(db.Model):
    __tablename__ = 'products'
    pid = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True)

with app.app_context():
    db.create_all()

# Auth Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

# Signup (NO QR here)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    if Users.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'User already exists'}), 409

    hashed_password = generate_password_hash(data['password'])
    secret = pyotp.random_base32()

    new_user = Users(username=data['username'], password=hashed_password, twofa_secret=secret)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Step 1 Login - Username & Password (returns QR base64 string)
@app.route('/login-step1', methods=['POST'])
def login_step1():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    user = Users.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate QR code for Google Authenticator
    otp_uri = pyotp.TOTP(user.twofa_secret).provisioning_uri(user.username, issuer_name="FlaskApp")
    qr_img = qrcode.make(otp_uri)
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')
0

# Step 2 Login - Submit OTP to get token
@app.route('/login-step2', methods=['POST'])
def login_step2():
    data = request.json
    if not data or 'username' not in data or 'otp' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    user = Users.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    totp = pyotp.TOTP(user.twofa_secret)
    if not totp.verify(data['otp']):
        return jsonify({'error': 'Invalid OTP'}), 401

    token = jwt.encode({
        'user': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({'token': token})

# CRUD Operations for Products
@app.route('/products', methods=['POST'])
@token_required
def create_product():
    data = request.json
    new_product = Products(
        pname=data['pname'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added'}), 201

@app.route('/products', methods=['GET'])
@token_required
def get_products():
    products = Products.query.all()
    return jsonify([{
        'id': p.pid,
        'name': p.pname,
        'description': p.description,
        'price': float(p.price),
        'stock': p.stock
    } for p in products])

@app.route('/products/<int:id>', methods=['PUT'])
@token_required
def update_product(id):
    product = Products.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.json
    product.pname = data.get('pname', product.pname)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return jsonify({'message': 'Product updated'})

@app.route('/products/<int:id>', methods=['DELETE'])
@token_required
def delete_product(id):
    product = Products.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})

if __name__ == '__main__':
    app.run(debug=True)
