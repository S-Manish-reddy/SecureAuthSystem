# SecureAuthSystem

A production-style secure authentication platform implementing JWT authentication, Multi-Factor Authentication (MFA/2FA), refresh token lifecycle management, brute-force protection, security analytics, and OWASP-aligned web security practices using FastAPI, PostgreSQL, HTML/CSS/JavaScript, and cloud deployment infrastructure.

---

# Features

## Authentication & Authorization

* User Registration & Login
* JWT Access Tokens
* Refresh Token Lifecycle Management
* Secure Logout System
* Protected API Routes
* Session Expiration Handling

---

## Security Features

* Password Hashing using bcrypt
* Rate Limiting
* Brute Force Protection
* Account Locking after Multiple Failed Attempts
* Security Event Logging
* Input Sanitization
* Secure Security Headers
* Content Security Policy (CSP)
* Trusted Host Validation
* CORS Security Configuration

---

## Multi-Factor Authentication (2FA)

* Google Authenticator Integration
* QR Code Generation
* OTP Verification
* MFA Enrollment Flow

---

## Security Monitoring

* Failed Login Analytics
* Security Event Tracking
* Attack Monitoring
* Login Statistics Dashboard Backend

---

## Frontend Features

* Secure Login Page
* Secure Registration Page
* Protected Dashboard
* Session Validation
* Automatic Logout on Token Expiration

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT (python-jose)
* Passlib / bcrypt

---

## Frontend

* HTML
* CSS
* JavaScript

---

## Security Libraries

* pyotp
* qrcode
* slowapi
* bleach

---

# Project Structure

```plaintext
SecureAuthSystem/
│
├── backend/
│   ├── auth/
│   ├── config/
│   ├── database/
│   ├── middleware/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── security/
│   ├── utils/
│   ├── logs/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── register.html
│   ├── dashboard.html
│   ├── verify-2fa.html
│   ├── style.css
│   └── app.js
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/SecureAuthSystem.git

cd SecureAuthSystem
```

---

# 2. Create Virtual Environment

## Windows CMD

```cmd
python -m venv venv

venv\Scripts\activate
```

---

# 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

---

# 4. Install PostgreSQL

Download and install PostgreSQL:

https://www.postgresql.org/download/

Create a database:

```plaintext
secure_auth_db
```

---

# 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/secure_auth_db

SECRET_KEY=YOUR_SECRET_KEY

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

# 6. Run Backend Server

```cmd
uvicorn backend.main:app --reload
```

Backend will run at:

```plaintext
http://127.0.0.1:8000
```

Swagger API Documentation:

```plaintext
http://127.0.0.1:8000/docs
```

---

# 7. Run Frontend

Install VS Code Live Server Extension.

Open:

```plaintext
frontend/index.html
```

Run using:

```plaintext
Open with Live Server
```

Frontend typically runs at:

```plaintext
http://127.0.0.1:5500
```

---

# Authentication Flow

## Registration

* User creates account
* Password is hashed using bcrypt
* User stored securely in PostgreSQL

---

## Login

* User enters credentials
* JWT Access Token generated
* Refresh Token generated
* Security logs recorded

---

## Protected Dashboard

* Frontend validates JWT
* Backend verifies token authenticity
* Unauthorized users blocked

---

## Two Factor Authentication

1. User enables 2FA
2. QR Code generated
3. Scan QR using Google Authenticator
4. Enter OTP code
5. MFA activated successfully

---

# API Endpoints

## Authentication Routes

| Endpoint    | Method | Description          |
| ----------- | ------ | -------------------- |
| `/register` | POST   | Register new user    |
| `/login`    | POST   | Login user           |
| `/logout`   | POST   | Logout user          |
| `/refresh`  | POST   | Refresh access token |

---

## User Routes

| Endpoint      | Method | Description            |
| ------------- | ------ | ---------------------- |
| `/profile`    | GET    | Protected user profile |
| `/enable-2fa` | POST   | Generate QR for MFA    |
| `/verify-2fa` | POST   | Verify OTP             |

---

## Security Monitoring Routes

| Endpoint           | Method | Description             |
| ------------------ | ------ | ----------------------- |
| `/security-events` | GET    | View security events    |
| `/security-stats`  | GET    | View security analytics |

---

# Security Features Explained

## Password Hashing

Passwords are securely hashed using bcrypt before storage.

---

## JWT Authentication

Short-lived JWT access tokens are used for secure authentication.

---

## Refresh Token Lifecycle

Refresh tokens allow secure session continuation without storing passwords.

---

## Rate Limiting

Limits repeated requests to mitigate brute-force attacks.

---

## Account Locking

Accounts are automatically locked after multiple failed login attempts.

---

## Content Security Policy

Helps mitigate Cross-Site Scripting (XSS) attacks.

---

## Input Sanitization

User input is sanitized using bleach to reduce XSS injection risks.

---

## Multi-Factor Authentication

Google Authenticator based OTP verification adds an additional security layer.

---

## Security Event Logging

Authentication and suspicious activities are logged for monitoring.

---

# Deployment

## Backend Deployment

Recommended:

* Render

---

## Frontend Deployment

Recommended:

* Vercel

---

## PostgreSQL Cloud Database

Recommended:

* Render PostgreSQL

---

# Important Security Notes

* Never commit `.env` file to GitHub.
* Always use HTTPS in production.
* Rotate secret keys periodically.
* Use strong passwords.
* Restrict CORS origins in production.
* Never expose database credentials publicly.

---

# Future Improvements

* React Frontend
* Redis Session Store
* Device-Based Sessions
* Email Verification
* Password Reset System
* Admin Dashboard UI
* Real-Time Attack Monitoring
* SIEM Integration
* Web Application Firewall (WAF)

---

# Author

Manish Reddy

---

# License

This project is intended for educational and cybersecurity learning purposes.
