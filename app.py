from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, send_from_directory
from flask_cors import CORS
import resend
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import re
from datetime import datetime, timedelta
import random
import string
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_this_in_production'
CORS(app)

resend.api_key = "re_G81rJoda_4yAmyTMaqdbbh9R58nt8U6ty"
RESEND_FROM_EMAIL = "noreply@pedulikulit.my.id"

# Upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flutter_app'
}

otp_storage = {}

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

def generate_otp():
    """Generate 6 digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp):
    """Kirim OTP ke email menggunakan Resend - Anti-Spam Version"""
    try:
        params = {
            "from": f"Peduli Kulit <{RESEND_FROM_EMAIL}>",
            "to": [email],
            "subject": "Kode Verifikasi Akun Anda",
            "html": f'''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verifikasi Email</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="padding: 40px 40px 30px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px 12px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">Verifikasi Email Anda</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <p style="margin: 0 0 20px; color: #333333; font-size: 16px; line-height: 1.6;">
                                Halo,
                            </p>
                            <p style="margin: 0 0 30px; color: #555555; font-size: 15px; line-height: 1.6;">
                                Terima kasih telah mendaftar di <strong>Peduli Kulit</strong>. Gunakan kode verifikasi berikut untuk melanjutkan proses pendaftaran Anda:
                            </p>
                            
                            <!-- OTP Box -->
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td align="center" style="padding: 20px 0;">
                                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="background-color: #f8f9fa; border: 2px solid #667eea; border-radius: 8px; padding: 20px 40px;">
                                            <tr>
                                                <td style="text-align: center;">
                                                    <span style="font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 8px; font-family: 'Courier New', Courier, monospace;">
                                                        {otp}
                                                    </span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Info -->
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top: 30px;">
                                <tr>
                                    <td style="padding: 15px; background-color: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
                                        <p style="margin: 0; color: #856404; font-size: 14px; line-height: 1.5;">
                                            <strong>Penting:</strong> Kode ini akan kedaluwarsa dalam 5 menit. Jangan bagikan kode ini kepada siapa pun.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 30px 0 0; color: #666666; font-size: 14px; line-height: 1.6;">
                                Jika Anda tidak melakukan permintaan ini, abaikan email ini. Akun Anda tetap aman.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 30px 40px; background-color: #f8f9fa; border-top: 1px solid #e9ecef; border-radius: 0 0 12px 12px;">
                            <p style="margin: 0 0 10px; color: #6c757d; font-size: 13px; line-height: 1.5; text-align: center;">
                                Email ini dikirim secara otomatis, mohon tidak membalas.
                            </p>
                            <p style="margin: 0; color: #adb5bd; font-size: 12px; text-align: center;">
                                &copy; 2024 Peduli Kulit. Semua hak dilindungi.
                            </p>
                        </td>
                    </tr>
                    
                </table>
                
                <!-- Spam Prevention Text (Hidden but read by spam filters) -->
                <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin-top: 20px;">
                    <tr>
                        <td style="text-align: center; color: #999999; font-size: 11px; line-height: 1.4;">
                            <p style="margin: 0;">
                                Email ini dikirim ke {email} karena Anda mendaftar di layanan kami.
                            </p>
                        </td>
                    </tr>
                </table>
                
            </td>
        </tr>
    </table>
</body>
</html>
            ''',
            
            "text": f'''
Verifikasi Email Anda

Halo,

Terima kasih telah mendaftar di Peduli Kulit. Gunakan kode verifikasi berikut untuk melanjutkan proses pendaftaran Anda:

Kode Verifikasi: {otp}

PENTING: Kode ini akan kedaluwarsa dalam 5 menit. Jangan bagikan kode ini kepada siapa pun.

Jika Anda tidak melakukan permintaan ini, abaikan email ini. Akun Anda tetap aman.

---
Email ini dikirim secara otomatis, mohon tidak membalas.
© 2024 Peduli Kulit. Semua hak dilindungi.

Email ini dikirim ke {email} karena Anda mendaftar di layanan kami.
            ''',
            "headers": {
                "X-Entity-Ref-ID": f"otp-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            },
            "tags": [
                {
                    "name": "category",
                    "value": "otp_verification"
                }
            ]
        }
        
        email_response = resend.Emails.send(params)
        print(f"✅ Email sent successfully to {email}")
        print(f"Resend response: {email_response}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

@app.route('/api/send-otp', methods=['POST'])
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

@app.route('/api/verify-otp', methods=['POST'])
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

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/register', methods=['POST'])
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

@app.route('/api/google-signin', methods=['POST'])
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
# ==================== ARTICLES API ====================

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Ambil semua artikel"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, title, description, image, created_at FROM articles ORDER BY created_at DESC")
        articles = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'data': articles}), 200
    except Exception as e:
        print(f"Error in get_articles: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500


@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """Ambil detail sebuah artikel"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, title, description, image, created_at FROM articles WHERE id = %s", (article_id,))
        article = cursor.fetchone()

        cursor.close()
        conn.close()

        if not article:
            return jsonify({'status': 'error', 'message': 'Artikel tidak ditemukan'}), 404

        return jsonify({'status': 'success', 'data': article}), 200
    except Exception as e:
        print(f"Error in get_article: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500


@app.route('/api/articles', methods=['POST'])
def create_article():
    """Buat artikel baru (sebaiknya dibatasi untuk admin)"""
    try:
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        image = data.get('image', '').strip() if data.get('image') else None

        if not title or not description:
            return jsonify({'status': 'error', 'message': 'Title dan description wajib diisi'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (title, description, image) VALUES (%s, %s, %s)", (title, description, image))
        conn.commit()
        article_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Artikel dibuat', 'data': {'id': article_id, 'title': title, 'description': description, 'image': image}}), 201
    except Exception as e:
        print(f"Error in create_article: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500


@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    """Update artikel (sebaiknya dibatasi untuk admin)"""
    try:
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        image = data.get('image', '').strip() if data.get('image') else None

        if not title or not description:
            return jsonify({'status': 'error', 'message': 'Title dan description wajib diisi'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("UPDATE articles SET title = %s, description = %s, image = %s WHERE id = %s", (title, description, image, article_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Artikel diperbarui'}), 200
    except Exception as e:
        print(f"Error in update_article: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500


@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """Hapus artikel (sebaiknya dibatasi untuk admin)"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = %s", (article_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Artikel dihapus'}), 200
    except Exception as e:
        print(f"Error in delete_article: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

# ==================== ARTICLES FAVORITE ====================

@app.route('/api/articles/<int:article_id>/favorite', methods=['POST'])
def favorite_article(article_id):
    user_id = request.json.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT IGNORE INTO article_favorites (user_id, article_id)
        VALUES (%s, %s)
    """, (user_id, article_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'success'})


@app.route('/api/articles/<int:article_id>/favorite', methods=['DELETE'])
def unfavorite_article(article_id):
    user_id = request.json.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM article_favorites
        WHERE user_id = %s AND article_id = %s
    """, (user_id, article_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'success'})


@app.route('/api/articles/<int:article_id>/favorite/status', methods=['GET'])
def article_favorite_status(article_id):
    user_id = request.args.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM article_favorites
        WHERE user_id = %s AND article_id = %s
        LIMIT 1
    """, (user_id, article_id))

    is_favorite = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return jsonify({'favorite': is_favorite})


@app.route('/api/articles/favorites', methods=['GET'])
def get_favorite_articles():
    try:
        user_id = int(request.args.get('user_id'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT a.*
            FROM articles a
            JOIN article_favorites af ON af.article_id = a.id
            WHERE af.user_id = %s
            ORDER BY af.id DESC
        """, (user_id,))

        articles = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'data': articles
        })

    except Exception as e:
        print("ERROR FAVORITE ARTICLES:", e)
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# ==================== PRODUCTS FAVORITE ====================

@app.route('/api/products/<int:product_id>/favorite', methods=['POST'])
def favorite_product(product_id):
    user_id = request.json.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT IGNORE INTO product_favorites (user_id, product_id)
        VALUES (%s, %s)
    """, (user_id, product_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'success'})


@app.route('/api/products/<int:product_id>/favorite', methods=['DELETE'])
def unfavorite_product(product_id):
    user_id = request.json.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM product_favorites
        WHERE user_id = %s AND product_id = %s
    """, (user_id, product_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'success'})


@app.route('/api/products/<int:product_id>/favorite/status', methods=['GET'])
def product_favorite_status(product_id):
    user_id = request.args.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM product_favorites
        WHERE user_id = %s AND product_id = %s
        LIMIT 1
    """, (user_id, product_id))

    is_favorite = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return jsonify({'favorite': is_favorite})


@app.route('/api/products/favorites', methods=['GET'])
def get_favorite_products():
    try:
        user_id = int(request.args.get('user_id'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT p.*
            FROM products p
            JOIN product_favorites pf ON pf.product_id = p.id
            WHERE pf.user_id = %s
            ORDER BY pf.id DESC
        """, (user_id,))

        products = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'data': products
        })

    except Exception as e:
        print("ERROR FAVORITE PRODUCTS:", e)
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ==================== PRODUCTS API ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Ambil semua products"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi FROM products ORDER BY id DESC")
        products = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'data': products}), 200
    except Exception as e:
        print(f"Error in get_products: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Ambil detail sebuah product"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()

        cursor.close()
        conn.close()

        if not product:
            return jsonify({'status': 'error', 'message': 'Product tidak ditemukan'}), 404

        return jsonify({'status': 'success', 'data': product}), 200
    except Exception as e:
        print(f"Error in get_product: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500


@app.route('/api/products', methods=['POST'])
def create_product():
    """Buat product baru (sebaiknya dibatasi untuk admin)"""
    try:
        data = request.get_json() or {}
        merek = data.get('merek', '').strip()
        nama = data.get('nama', '').strip()
        harga = data.get('harga')
        kategori_penyakit = data.get('kategori_penyakit', '').strip()
        image = data.get('image', '').strip() if data.get('image') else None
        deskripsi = data.get('deskripsi', '').strip() if data.get('deskripsi') else None
        dosis = data.get('dosis', '').strip() if data.get('dosis') else None
        efek_samping = data.get('efek_samping', '').strip() if data.get('efek_samping') else None
        komposisi = data.get('komposisi', '').strip() if data.get('komposisi') else None
        manufaktur = data.get('manufaktur', '').strip() if data.get('manufaktur') else None
        nomor_registrasi = data.get('nomor_registrasi', '').strip() if data.get('nomor_registrasi') else None

        if not merek or not nama or harga is None or not kategori_penyakit:
            return jsonify({'status': 'error', 'message': 'Field wajib diisi'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi))
        conn.commit()
        product_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Product dibuat', 'data': {'id': product_id, 'merek': merek, 'nama': nama, 'harga': harga, 'kategori_penyakit': kategori_penyakit, 'image': image, 'deskripsi': deskripsi, 'dosis': dosis, 'efek_samping': efek_samping, 'komposisi': komposisi, 'manufaktur': manufaktur, 'nomor_registrasi': nomor_registrasi}}), 201
    except Exception as e:
        print(f"Error in create_product: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500


@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product (sebaiknya dibatasi untuk admin)"""
    try:
        data = request.get_json() or {}
        merek = data.get('merek', '').strip()
        nama = data.get('nama', '').strip()
        harga = data.get('harga')
        kategori_penyakit = data.get('kategori_penyakit', '').strip()
        image = data.get('image', '').strip() if data.get('image') else None
        deskripsi = data.get('deskripsi', '').strip() if data.get('deskripsi') else None
        dosis = data.get('dosis', '').strip() if data.get('dosis') else None
        efek_samping = data.get('efek_samping', '').strip() if data.get('efek_samping') else None
        komposisi = data.get('komposisi', '').strip() if data.get('komposisi') else None
        manufaktur = data.get('manufaktur', '').strip() if data.get('manufaktur') else None
        nomor_registrasi = data.get('nomor_registrasi', '').strip() if data.get('nomor_registrasi') else None

        if not merek or not nama or harga is None or not kategori_penyakit:
            return jsonify({'status': 'error', 'message': 'Field wajib diisi'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("UPDATE products SET merek = %s, nama = %s, harga = %s, kategori_penyakit = %s, image = %s, deskripsi = %s, dosis = %s, efek_samping = %s, komposisi = %s, manufaktur = %s, nomor_registrasi = %s WHERE id = %s", (merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi, product_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Product diperbarui'}), 200
    except Exception as e:
        print(f"Error in update_product: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Hapus product (sebaiknya dibatasi untuk admin)"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Product dihapus'}), 200
    except Exception as e:
        print(f"Error in delete_product: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500
    
# ==================== WEB INTERFACE ROUTES ====================

def login_required(f):
    """Decorator untuk memastikan user sudah login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Silakan login terlebih dahulu', 'warning')
            return redirect(url_for('web_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== WEB LOGIN ====================

@app.route('/web/login', methods=['GET', 'POST'])
def web_login():
    """Halaman login untuk admin"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email dan password wajib diisi', 'danger')
            return redirect(url_for('web_login'))
        
        try:
            conn = get_db_connection()
            if not conn:
                flash('Gagal terhubung ke database', 'danger')
                return redirect(url_for('web_login'))
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s AND is_admin = 1", (email,))
            admin = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if admin and check_password_hash(admin['password'], password):
                session['admin_id'] = admin['id']
                session['admin_name'] = admin['name']
                flash(f'Selamat datang, {admin["name"]}!', 'success')
                return redirect(url_for('web_dashboard'))
            else:
                flash('Email atau password salah, atau Anda bukan admin', 'danger')
        except Exception as e:
            print(f"Error in web_login: {e}")
            flash('Terjadi kesalahan server', 'danger')
    
    return render_template('web_login.html')

# ==================== WEB LOGOUT ====================

@app.route('/web/logout')
def web_logout():
    """Logout dari admin"""
    session.clear()
    flash('Anda berhasil logout', 'success')
    return redirect(url_for('web_login'))

# ==================== WEB DASHBOARD ====================

@app.route('/web')
@app.route('/web/dashboard')
@login_required
def web_dashboard():
    """Dashboard utama - menampilkan statistik"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_login'))
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = 0")
        total_users = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM skin_data")
        total_records = cursor.fetchone()['count']
        
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE is_admin = 0 ORDER BY created_at DESC LIMIT 5")
        recent_users = cursor.fetchall()

        cursor.execute("SELECT skin_condition, COUNT(*) as count FROM skin_data GROUP BY skin_condition")
        skin_stats = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('web_dashboard.html', 
                             total_users=total_users,
                             total_records=total_records,
                             recent_users=recent_users,
                             skin_stats=skin_stats)
    except Exception as e:
        print(f"Error in web_dashboard: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_login'))
    
# ==================== WEB USERS ====================

@app.route('/web/users')
@login_required
def web_users():
    """Halaman manajemen users"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_dashboard'))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE is_admin = 0 ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('web_users.html', users=users)
    except Exception as e:
        print(f"Error in web_users: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_dashboard'))

@app.route('/web/users/<int:user_id>')
@login_required
def web_user_detail(user_id):
    """Halaman detail user"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_users'))
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = %s AND is_admin = 0", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            flash('User tidak ditemukan', 'warning')
            return redirect(url_for('web_users'))
        
        cursor.execute("""
            SELECT id, skin_condition, severity, notes, created_at 
            FROM skin_data 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (user_id,))
        skin_records = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('web_user_detail.html', user=user, skin_records=skin_records)
    except Exception as e:
        print(f"Error in web_user_detail: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_users'))

@app.route('/web/users/<int:user_id>/delete', methods=['POST'])
@login_required
def web_delete_user(user_id):
    """Hapus user"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_users'))
        
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM skin_data WHERE user_id = %s", (user_id,))
        
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash(f'User berhasil dihapus', 'success')
        return redirect(url_for('web_users'))
    except Exception as e:
        print(f"Error in web_delete_user: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_users'))

@app.route('/web/users/bulk-delete', methods=['POST'])
@login_required
def web_bulk_delete_users():
    """Bulk hapus users dari admin dashboard"""
    try:
        user_ids = request.form.getlist('user_ids')

        if not user_ids:
            flash('Tidak ada user yang dipilih', 'warning')
            return redirect(url_for('web_users'))

        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_users'))

        cursor = conn.cursor()

        # Delete related skin_data first
        placeholders = ','.join(['%s'] * len(user_ids))
        cursor.execute(f"DELETE FROM skin_data WHERE user_id IN ({placeholders})", user_ids)

        # Then delete users
        cursor.execute(f"DELETE FROM users WHERE id IN ({placeholders})", user_ids)
        deleted_count = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        flash(f'{deleted_count} user berhasil dihapus', 'success')
        return redirect(url_for('web_users'))
    except Exception as e:
        print(f"Error in web_bulk_delete_users: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_users'))

# ==================== WEB ARTICLES ====================

@app.route('/web/articles')
@login_required
def web_articles():
    """Halaman manajemen artikel"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_dashboard'))

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, title, description, image, created_at FROM articles ORDER BY created_at DESC")
        articles = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('web_articles.html', articles=articles)
    except Exception as e:
        print(f"Error in web_articles: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_dashboard'))


@app.route('/web/articles/create', methods=['GET', 'POST'])
@login_required
def web_create_article():
    """Buat artikel baru melalui admin dashboard"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_filename = filename

        if not title or not description:
            flash('Title dan description wajib diisi', 'danger')
            return redirect(url_for('web_create_article'))

        try:
            conn = get_db_connection()
            if not conn:
                flash('Gagal terhubung ke database', 'danger')
                return redirect(url_for('web_articles'))

            cursor = conn.cursor()
            cursor.execute("INSERT INTO articles (title, description, image) VALUES (%s, %s, %s)", (title, description, image_filename))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Artikel berhasil dibuat', 'success')
            return redirect(url_for('web_articles'))
        except Exception as e:
            print(f"Error in web_create_article: {e}")
            flash('Terjadi kesalahan server', 'danger')
            return redirect(url_for('web_articles'))

    return render_template('web_article_form.html', article=None)


@app.route('/web/articles/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def web_edit_article(article_id):
    """Edit artikel melalui admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_articles'))

        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    image_filename = filename
            
            if not image_filename:
                cursor.execute("SELECT image FROM articles WHERE id = %s", (article_id,))
                current = cursor.fetchone()
                image_filename = current['image'] if current else None

            if not title or not description:
                flash('Title dan description wajib diisi', 'danger')
                cursor.close()
                conn.close()
                return redirect(url_for('web_edit_article', article_id=article_id))

            cursor.execute("UPDATE articles SET title = %s, description = %s, image = %s WHERE id = %s", (title, description, image_filename, article_id))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Artikel berhasil diperbarui', 'success')
            return redirect(url_for('web_articles'))

        cursor.execute("SELECT id, title, description, image, created_at FROM articles WHERE id = %s", (article_id,))
        article = cursor.fetchone()

        cursor.close()
        conn.close()

        if not article:
            flash('Artikel tidak ditemukan', 'warning')
            return redirect(url_for('web_articles'))

        return render_template('web_article_form.html', article=article)
    except Exception as e:
        print(f"Error in web_edit_article: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_articles'))


@app.route('/web/articles/<int:article_id>/delete', methods=['POST'])
@login_required
def web_delete_article(article_id):
    """Hapus artikel dari admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_articles'))

        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = %s", (article_id,))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Artikel berhasil dihapus', 'success')
        return redirect(url_for('web_articles'))
    except Exception as e:
        print(f"Error in web_delete_article: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_articles'))

@app.route('/web/articles/bulk-delete', methods=['POST'])
@login_required
def web_bulk_delete_articles():
    """Bulk hapus articles dari admin dashboard"""
    try:
        article_ids = request.form.getlist('article_ids')

        if not article_ids:
            flash('Tidak ada artikel yang dipilih', 'warning')
            return redirect(url_for('web_articles'))

        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_articles'))

        cursor = conn.cursor()

        # Create placeholders for the IN clause
        placeholders = ','.join(['%s'] * len(article_ids))
        cursor.execute(f"DELETE FROM articles WHERE id IN ({placeholders})", article_ids)
        deleted_count = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        flash(f'{deleted_count} artikel berhasil dihapus', 'success')
        return redirect(url_for('web_articles'))
    except Exception as e:
        print(f"Error in web_bulk_delete_articles: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_articles'))

# ==================== WEB PRODUCTS ====================
    
@app.route('/web/products')
@login_required
def web_products():
    """Halaman manajemen product"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_dashboard'))

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi FROM products ORDER BY id DESC")
        products = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('web_products.html', products=products)
    except Exception as e:
        print(f"Error in web_products: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_dashboard'))


@app.route('/web/products/create', methods=['GET', 'POST'])
@login_required
def web_create_product():
    """Buat product baru melalui admin dashboard"""
    if request.method == 'POST':
        merek = request.form.get('merek', '').strip()
        nama = request.form.get('nama', '').strip()
        harga = request.form.get('harga', '').strip()
        kategori_penyakit = request.form.get('kategori_penyakit', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip() or None
        dosis = request.form.get('dosis', '').strip() or None
        efek_samping = request.form.get('efek_samping', '').strip() or None
        komposisi = request.form.get('komposisi', '').strip() or None
        manufaktur = request.form.get('manufaktur', '').strip() or None
        nomor_registrasi = request.form.get('nomor_registrasi', '').strip() or None
        
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_filename = filename

        if not merek or not nama or not harga or not kategori_penyakit:
            flash('Merek, nama, harga, dan kategori penyakit wajib diisi', 'danger')
            return redirect(url_for('web_create_product'))

        try:
            conn = get_db_connection()
            if not conn:
                flash('Gagal terhubung ke database', 'danger')
                return redirect(url_for('web_products'))

            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (merek, nama, harga, kategori_penyakit, image_filename, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Produk berhasil dibuat', 'success')
            return redirect(url_for('web_products'))
        except Exception as e:
            print(f"Error in web_create_product: {e}")
            flash('Terjadi kesalahan server', 'danger')
            return redirect(url_for('web_products'))

    return render_template('web_product_form.html', product=None)

@app.route('/web/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def web_edit_product(product_id):
    """Edit product melalui admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_products'))

        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            merek = request.form.get('merek', '').strip()
            nama = request.form.get('nama', '').strip()
            harga = request.form.get('harga', '').strip()
            kategori_penyakit = request.form.get('kategori_penyakit', '').strip()
            deskripsi = request.form.get('deskripsi', '').strip() or None
            dosis = request.form.get('dosis', '').strip() or None
            efek_samping = request.form.get('efek_samping', '').strip() or None
            komposisi = request.form.get('komposisi', '').strip() or None
            manufaktur = request.form.get('manufaktur', '').strip() or None
            nomor_registrasi = request.form.get('nomor_registrasi', '').strip() or None
            
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    image_filename = filename
            
            if not image_filename:
                cursor.execute("SELECT image FROM products WHERE id = %s", (product_id,))
                current = cursor.fetchone()
                image_filename = current['image'] if current else None

            if not merek or not nama or not harga or not kategori_penyakit:
                flash('Merek, nama, harga, dan kategori penyakit wajib diisi', 'danger')
                cursor.close()
                conn.close()
                return redirect(url_for('web_edit_product', product_id=product_id))

            cursor.execute("UPDATE products SET merek = %s, nama = %s, harga = %s, kategori_penyakit = %s, image = %s, deskripsi = %s, dosis = %s, efek_samping = %s, komposisi = %s, manufaktur = %s, nomor_registrasi = %s WHERE id = %s", (merek, nama, harga, kategori_penyakit, image_filename, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi, product_id))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Produk berhasil diperbarui', 'success')
            return redirect(url_for('web_products'))

        cursor.execute("SELECT id, merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()

        cursor.close()
        conn.close()

        if not product:
            flash('Produk tidak ditemukan', 'warning')
            return redirect(url_for('web_products'))

        return render_template('web_product_form.html', product=product)
    except Exception as e:
        print(f"Error in web_edit_product: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_products'))


@app.route('/web/products/<int:product_id>/delete', methods=['POST'])
@login_required
def web_delete_product(product_id):
    """Hapus product dari admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_product'))

        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Produk berhasil dihapus', 'success')
        return redirect(url_for('web_products'))
    except Exception as e:
        print(f"Error in web_delete_article: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_products'))

@app.route('/web/products/bulk-delete', methods=['POST'])
@login_required
def web_bulk_delete_products():
    """Bulk hapus products dari admin dashboard"""
    try:
        product_ids = request.form.getlist('product_ids')

        if not product_ids:
            flash('Tidak ada produk yang dipilih', 'warning')
            return redirect(url_for('web_products'))

        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_products'))

        cursor = conn.cursor()

        # Create placeholders for the IN clause
        placeholders = ','.join(['%s'] * len(product_ids))
        cursor.execute(f"DELETE FROM products WHERE id IN ({placeholders})", product_ids)
        deleted_count = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        flash(f'{deleted_count} produk berhasil dihapus', 'success')
        return redirect(url_for('web_products'))
    except Exception as e:
        print(f"Error in web_bulk_delete_products: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_products'))

# ==================== WEB SKIN DATA ====================

@app.route('/web/skin-data')
@login_required
def web_skin_data():
    """Halaman manajemen data kulit"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_dashboard'))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT sd.id, sd.user_id, sd.skin_condition, sd.severity, sd.notes, sd.created_at, u.name
            FROM skin_data sd
            JOIN users u ON sd.user_id = u.id
            ORDER BY sd.created_at DESC
        """)
        skin_data = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('web_skin_data.html', skin_data=skin_data)
    except Exception as e:
        print(f"Error in web_skin_data: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_dashboard'))

@app.route('/web/skin-data/<int:record_id>/delete', methods=['POST'])
@login_required
def web_delete_skin_record(record_id):
    """Hapus record kulit"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_skin_data'))
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM skin_data WHERE id = %s", (record_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Record kulit berhasil dihapus', 'success')
        return redirect(url_for('web_skin_data'))
    except Exception as e:
        print(f"Error in web_delete_skin_record: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_skin_data'))
    
# ==================== WEB SETTINGS ====================

@app.route('/web/settings')
@login_required
def web_settings():
    """Halaman pengaturan"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_dashboard'))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (session.get('admin_id'),))
        admin = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('web_settings.html', admin=admin)
    except Exception as e:
        print(f"Error in web_settings: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_dashboard'))

@app.route('/web/settings/update-password', methods=['POST'])
@login_required
def web_update_password():
    """Update password admin"""
    try:
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        admin_id = session.get('admin_id')
        
        if not old_password or not new_password or not confirm_password:
            flash('Semua field wajib diisi', 'danger')
            return redirect(url_for('web_settings'))
        
        if new_password != confirm_password:
            flash('Password baru tidak cocok', 'danger')
            return redirect(url_for('web_settings'))
        
        if len(new_password) < 6:
            flash('Password minimal 6 karakter', 'danger')
            return redirect(url_for('web_settings'))
        
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_settings'))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password FROM users WHERE id = %s", (admin_id,))
        admin = cursor.fetchone()
        
        if not admin or not check_password_hash(admin['password'], old_password):
            flash('Password lama salah', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('web_settings'))
        
        hashed_password = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, admin_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Password berhasil diubah', 'success')
        return redirect(url_for('web_settings'))
    except Exception as e:
        print(f"Error in web_update_password: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_settings'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)