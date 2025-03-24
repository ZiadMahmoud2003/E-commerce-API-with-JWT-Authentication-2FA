# E-commerce API with JWT Authentication & 2FA

This is a secure REST API built with **Flask**, featuring **JWT authentication**, **two-factor authentication (2FA) using Google Authenticator**, and CRUD operations for an e-commerce **Products** table.

## Features
- User registration with password hashing
- Two-factor authentication (2FA) using Google Authenticator
- JWT-based authentication for secure API access
- CRUD operations for managing products
- Token-based authorization middleware

## Technologies Used
- **Python** & **Flask**
- **Flask-SQLAlchemy** (ORM for MySQL database)
- **JWT (JSON Web Token) Authentication**
- **PyOTP** (For 2FA generation and verification)
- **QR Code Generation** (For Google Authenticator setup)
- **MySQL** (Database)

---

## Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/ZiadMahmoud2003/E-commerce API with JWT Authentication & 2FA.git
cd E-commerce API with JWT Authentication & 2FA
```

### 2️⃣ Create a Virtual Environment & Install Dependencies
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Set Up MySQL Database
1. Start MySQL Server
2. Create a database named `ecommerce`:
   ```sql
   CREATE DATABASE ecommerce;
   ```
3. Update `app.config['SQLALCHEMY_DATABASE_URI']` in `app.py` with your MySQL credentials:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ecommerce'
   ```
4. Initialize the database:
   ```sh
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

### 4️⃣ Run the Flask Application
```sh
python app.py
```
By default, the app will run on `http://127.0.0.1:5000`.

---

## API Endpoints

### 🔹 User Authentication
#### ➤ Register a User
**POST** `/signup`
```json
{
  "username": "testuser",
  "password": "password123"
}
```
_Response:_
```json
{
  "message": "User registered",
  "2FA_secret": "JBSWY3DPEHPK3PXP"
}
```

#### ➤ Generate QR Code for Google Authenticator
**GET** `/generate_qr/<username>`

_Response:_ Returns a QR code to scan with **Google Authenticator**.

#### ➤ Login with 2FA
**POST** `/login`
```json
{
  "username": "testuser",
  "password": "password123",
  "otp": "123456"
}
```
_Response:_
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```

---

### 🔹 CRUD Operations for Products (Requires JWT Token)
#### ➤ Create a Product
**POST** `/products`
```json
{
  "pname": "Laptop",
  "description": "A powerful laptop",
  "price": 1200.99,
  "stock": 10
}
```
#### ➤ Get All Products
**GET** `/products`

#### ➤ Update a Product
**PUT** `/products/<pid>`
```json
{
  "pname": "Gaming Laptop",
  "price": 1500.00
}
```
#### ➤ Delete a Product
**DELETE** `/products/<pid>`

---

## Testing
You can test the API using:
- **Postman**
- **cURL**
- **Python requests module**

### Example cURL Request (Login)
```sh
curl -X POST http://127.0.0.1:5000/login \  
     -H "Content-Type: application/json" \  
     -d '{"username": "testuser", "password": "password123", "otp": "123456"}'
```

---

## License
This project is open-source and available under the MIT License.

---

## Author
**Ziad Abdelgwad** - [GitHub](https://github.com/ZiadMahmoud2003)

