from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import (
    get_db_connection,
    validate_email,
    generate_otp,
    send_otp_email,
    otp_storage,
)
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# =========================
# OTP
# =========================

@auth_bp.route('/api/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify(status='error', message='Mohon masukkan email'), 400
    if not validate_email(email):
        return jsonify(status='error', message='Email tidak valid'), 400

    conn = get_db_connection()
    if not conn:
        return jsonify(status='error', message='DB error'), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify(status='error', message='Email sudah terdaftar'), 409

    if email in otp_storage:
        last = otp_storage[email]['created_at']
        diff = (datetime.now() - last).total_seconds()
        if diff < 60:
            return jsonify(
                status='error',
                message=f'Tunggu {int(60 - diff)} detik'
            ), 429

    otp = generate_otp()
    otp_storage[email] = {
        'otp': otp,
        'expires_at': datetime.now() + timedelta(minutes=5),
        'created_at': datetime.now(),
    }

    if not send_otp_email(email, otp):
        return jsonify(status='error', message='Gagal kirim email'), 500

    return jsonify(status='success', message='OTP terkirim'), 200


@auth_bp.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    otp = data.get('otp', '').strip()

    if not email or not otp:
        return jsonify(status='error', message='Data tidak lengkap'), 400

    stored = otp_storage.get(email)
    if not stored:
        return jsonify(status='error', message='OTP tidak ditemukan'), 400
    if datetime.now() > stored['expires_at']:
        del otp_storage[email]
        return jsonify(status='error', message='OTP kadaluarsa'), 400
    if stored['otp'] != otp:
        return jsonify(status='error', message='OTP salah'), 400

    return jsonify(status='success', message='OTP valid'), 200


# =========================
# REGISTER
# =========================

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    otp = data.get('otp', '').strip()

    if not all([name, email, password, otp]):
        return jsonify(status='error', message='Data tidak lengkap'), 400
    if not validate_email(email):
        return jsonify(status='error', message='Email tidak valid'), 400
    if len(password) < 6:
        return jsonify(status='error', message='Password minimal 6 karakter'), 400

    stored = otp_storage.get(email)
    if not stored or stored['otp'] != otp:
        return jsonify(status='error', message='OTP tidak valid'), 400
    if datetime.now() > stored['expires_at']:
        del otp_storage[email]
        return jsonify(status='error', message='OTP kadaluarsa'), 400

    conn = get_db_connection()
    if not conn:
        return jsonify(status='error', message='DB error'), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify(status='error', message='Email sudah terdaftar'), 409

    hashed = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
        (name, email, hashed),
    )
    conn.commit()
    user_id = cursor.lastrowid

    cursor.close()
    conn.close()
    del otp_storage[email]

    access_token = create_access_token(identity=str(user_id))

    return jsonify(
        status='success',
        data={
            'id': user_id,
            'name': name,
            'email': email,
            'access_token': access_token,
        },
    ), 201


# =========================
# LOGIN (JWT FIX)
# =========================

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify(status='error', message='Data tidak lengkap'), 400

    conn = get_db_connection()
    if not conn:
        return jsonify(status='error', message='DB error'), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or not check_password_hash(user['password'], password):
        return jsonify(status='error', message='Login gagal'), 401

    access_token = create_access_token(identity=str(user['id']))

    return jsonify(
        status='success',
        data={
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'access_token': access_token,
        },
    ), 200


# =========================
# GOOGLE SIGN-IN (JWT FIX)
# =========================

@auth_bp.route('/api/google-signin', methods=['POST'])
def google_signin():
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    google_id = data.get('google_id', '').strip()

    if not all([name, email, google_id]):
        return jsonify(status='error', message='Data tidak lengkap'), 400
    if not validate_email(email):
        return jsonify(status='error', message='Email tidak valid'), 400

    conn = get_db_connection()
    if not conn:
        return jsonify(status='error', message='DB error'), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        access_token = create_access_token(identity=str(user['id']))
        cursor.close()
        conn.close()
        return jsonify(
            status='success',
            data={**user, 'access_token': access_token},
        ), 200

    hashed = generate_password_hash(google_id)
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
        (name, email, hashed),
    )
    conn.commit()
    user_id = cursor.lastrowid

    cursor.close()
    conn.close()

    access_token = create_access_token(identity=str(user_id))

    return jsonify(
        status='success',
        data={
            'id': user_id,
            'name': name,
            'email': email,
            'access_token': access_token,
        },
    ), 201
