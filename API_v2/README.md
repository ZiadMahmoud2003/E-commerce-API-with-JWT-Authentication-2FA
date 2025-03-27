# 🛡️ Flask JWT & 2FA API with Product CRUD

This project is a secure Flask-based RESTful API that supports:

- 🔐 User registration with password hashing and 2FA setup  
- 🔑 Login with JWT authentication and OTP verification (Google Authenticator)  
- 🛒 Full CRUD operations for managing products  
- ✅ Token-based authorization for protected routes  

---

## 📦 Tech Stack

- Python + Flask  
- SQLAlchemy ORM + MySQL  
- JWT Authentication  
- Google Authenticator (2FA via `pyotp`)  
- QR code generation with `qrcode` & `Pillow`  

---

## 🚀 Features

- 🔒 Secure user registration with password hashing  
- 🧠 Two-step login process with OTP verification  
- 🔐 JWT token generation for session management  
- 🛒 Product management with Create, Read, Update, Delete  
- ⚙️ MySQL as the database  

---

## 🛠️ Installation & Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/flask-2fa-api.git
cd flask-2fa-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install Flask Flask-SQLAlchemy PyMySQL pyotp qrcode pillow pyjwt
```

### 3. Set up MySQL

Create a database called `ecommerce`:

```sql
CREATE DATABASE ecommerce;
```

Update the DB URI in `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ecommerce'
```

### 4. Run the app

```bash
python app.py
```

---

## 🔐 Authentication Flow

### 1️⃣ Register

**POST** `/signup`

```json
{
  "username": "testuser",
  "password": "testpass"
}
```

Returns: ✅ `User registered successfully`

---

### 2️⃣ Login Step 1 - Get QR Code

**POST** `/login-step1`

```json
{
  "username": "testuser",
  "password": "testpass"
}
```

Returns: PNG image (QR code) – scan with Google Authenticator.

---

### 3️⃣ Login Step 2 - Verify OTP

**POST** `/login-step2`

```json
{
  "username": "testuser",
  "otp": "123456"
}
```

Returns:

```json
{
  "token": "your-jwt-token"
}
```

Use this token for authorization in protected routes.

---

## 🛒 Product API (JWT Protected)

Include the token in the header:

```
Authorization: your-jwt-token
```

### ➕ Create Product

**POST** `/products`

```json
{
  "pname": "iPhone 14",
  "description": "Apple smartphone",
  "price": 999.99,
  "stock": 10
}
```

---

### 📃 Get All Products

**GET** `/products`

---

### ✏️ Update Product

**PUT** `/products/<id>`

```json
{
  "price": 899.99,
  "stock": 5
}
```

---

### ❌ Delete Product

**DELETE** `/products/<id>`

---

## 📂 Project Structure

```
📁 flask-2fa-api
├── app.py
├── requirements.txt
└── README.md
