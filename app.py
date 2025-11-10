from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS untuk Flutter

# Konfigurasi Database XAMPP
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # default XAMPP
    'password': '',  # default XAMPP kosong
    'database': 'flutter_app'
}

def get_db_connection():
    """Membuat koneksi ke database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def validate_email(email):
    """Validasi format email"""
    pattern = r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'
    return re.match(pattern, email) is not None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint untuk cek server status"""
    return jsonify({
        'status': 'success',
        'message': 'Server is running',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/register', methods=['POST'])
def register():
    """Endpoint untuk registrasi user baru"""
    try:
        data = request.get_json()
        
        # Validasi input
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
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
        
        # Koneksi ke database
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'status': 'error',
                'message': 'Gagal terhubung ke database'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        # Cek apakah email sudah terdaftar
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({
                'status': 'error',
                'message': 'Email sudah terdaftar'
            }), 409
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Insert user baru
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, hashed_password))
        conn.commit()
        
        user_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
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

@app.route('/api/login', methods=['POST'])
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
        
        # Koneksi ke database
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'status': 'error',
                'message': 'Gagal terhubung ke database'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        # Cari user berdasarkan email
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

@app.route('/api/users/<int:user_id>', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)