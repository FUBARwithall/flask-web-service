from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db_connection, validate_email, generate_otp, send_otp_email, otp_storage
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/send-otp', methods=['POST'])
def send_otp():
    """Endpoint untuk mengirim OTP ke email"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({
                'status': 'error',
                'message': 'Mohon masukkan email'
            }), 400
        
        if not validate_email(email):
            return jsonify({
                'status': 'error',
                'message': 'Mohon masukkan email yang valid'
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'status': 'error',
                'message': 'Gagal terhubung ke database'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if existing_user:
            return jsonify({
                'status': 'error',
                'message': 'Email sudah terdaftar'
            }), 409
        
        if email in otp_storage:
            last_request = otp_storage[email].get('created_at', datetime.now() - timedelta(minutes=10))
            time_diff = (datetime.now() - last_request).total_seconds()
            
            if time_diff < 60:
                wait_time = int(60 - time_diff)
                return jsonify({
                    'status': 'error',
                    'message': f'Mohon tunggu {wait_time} detik sebelum meminta OTP lagi'
                }), 429
        
        otp = generate_otp()
        otp_storage[email] = {
            'otp': otp,
            'expires_at': datetime.now() + timedelta(minutes=5),
            'created_at': datetime.now()
        }
        
        print(f"=== OTP untuk {email}: {otp} ===")
        
        if send_otp_email(email, otp):
            return jsonify({
                'status': 'success',
                'message': f'Kode OTP telah dikirim ke {email}. Silakan cek inbox atau folder spam Anda.'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Gagal mengirim email. Silakan coba lagi.'
            }), 500
        
    except Exception as e:
        print(f"Error in send_otp: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server'
        }), 500

@auth_bp.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    """Endpoint untuk verifikasi OTP"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        otp = data.get('otp', '').strip()
        
        if not email or not otp:
            return jsonify({
                'status': 'error',
                'message': 'Email dan OTP wajib diisi'
            }), 400
        
        if email not in otp_storage:
            return jsonify({
                'status': 'error',
                'message': 'OTP tidak ditemukan atau sudah kadaluarsa'
            }), 400
        
        stored_data = otp_storage[email]
        
        if datetime.now() > stored_data['expires_at']:
            del otp_storage[email]
            return jsonify({
                'status': 'error',
                'message': 'OTP sudah kadaluarsa. Silakan minta OTP baru.'
            }), 400
        
        if stored_data['otp'] != otp:
            return jsonify({
                'status': 'error',
                'message': 'Kode OTP salah'
            }), 400
        
        return jsonify({
            'status': 'success',
            'message': 'OTP berhasil diverifikasi'
        }), 200
        
    except Exception as e:
        print(f"Error in verify_otp: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server'
        }), 500

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """Endpoint untuk registrasi user baru"""
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        otp = data.get('otp', '').strip()
        
        if not name:
            return jsonify({
                'status': 'error',
                'message': 'Mohon masukkan nama lengkap'
            }), 400
        
        if not email:
            return jsonify({
                'status': 'error',
                'message': 'Mohon masukkan email'
            }), 400
        
        if not validate_email(email):
            return jsonify({
                'status': 'error',
                'message': 'Mohon masukkan email yang valid'
            }), 400
        
        if not password or len(password) < 6:
            return jsonify({
                'status': 'error',
                'message': 'Kata sandi minimal 6 karakter'
            }), 400
        
        if not otp:
            return jsonify({
                'status': 'error',
                'message': 'Kode OTP wajib diisi'
            }), 400
        
        if email not in otp_storage:
            return jsonify({
                'status': 'error',
                'message': 'OTP tidak valid atau sudah kadaluarsa'
            }), 400
        
        stored_data = otp_storage[email]
        
        if datetime.now() > stored_data['expires_at']:
            del otp_storage[email]
            return jsonify({
                'status': 'error',
                'message': 'OTP sudah kadaluarsa'
            }), 400
        
        if stored_data['otp'] != otp:
            return jsonify({
                'status': 'error',
                'message': 'Kode OTP salah'
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'status': 'error',
                'message': 'Gagal terhubung ke database'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({
                'status': 'error',
                'message': 'Email sudah terdaftar'
            }), 409
        
        hashed_password = generate_password_hash(password)
        
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, hashed_password))
        conn.commit()
        
        user_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        del otp_storage[email]
        
        return jsonify({
            'status': 'success',
            'message': 'Pendaftaran berhasil! Selamat datang 👋',
            'data': {
                'id': user_id,
                'name': name,
                'email': email
            }
        }), 201
        
    except Exception as e:
        print(f"Error in register: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server'
        }), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Endpoint untuk login"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'status': 'error',
                'message': 'Email dan password wajib diisi'
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'status': 'error',
                'message': 'Gagal terhubung ke database'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not user or not check_password_hash(user['password'], password):
            return jsonify({
                'status': 'error',
                'message': 'Email atau password salah'
            }), 401
        
        return jsonify({
            'status': 'success',
            'message': 'Login berhasil',
            'data': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server'
        }), 500

@auth_bp.route('/api/google-signin', methods=['POST'])
def google_signin():
    """Endpoint untuk Google Sign-In - simpan atau login user"""
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        google_id = data.get('google_id', '').strip()
        
        if not name or not email or not google_id:
            return jsonify({
                'status': 'error',
                'message': 'Data tidak lengkap'
            }), 400
        
        if not validate_email(email):
            return jsonify({
                'status': 'error',
                'message': 'Email tidak valid'
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'status': 'error',
                'message': 'Gagal terhubung ke database'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT id, name, email FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({
                'status': 'success',
                'message': 'Login berhasil',
                'data': {
                    'id': existing_user['id'],
                    'name': existing_user['name'],
                    'email': existing_user['email']
                }
            }), 200
        
        random_password = generate_password_hash(google_id)
        
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, random_password))
        conn.commit()
        
        user_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Pendaftaran berhasil dengan Google!',
            'data': {
                'id': user_id,
                'name': name,
                'email': email
            }
        }), 201
        
    except Exception as e:
        print(f"Error in google_signin: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server'
        }), 500

@auth_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Endpoint untuk mendapatkan detail user"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'status': 'error',
                'message': 'Gagal terhubung ke database'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User tidak ditemukan'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': user
        }), 200
        
    except Exception as e:
        print(f"Error in get_user: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Terjadi kesalahan server'
        }), 500