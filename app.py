from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_this_in_production'
CORS(app)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
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

@app.route('/web/logout')
def web_logout():
    """Logout dari admin"""
    session.clear()
    flash('Anda berhasil logout', 'success')
    return redirect(url_for('web_login'))

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