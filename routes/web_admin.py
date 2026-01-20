from urllib.parse import unquote
from flask import Blueprint, request, render_template, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
import os
from models import get_db_connection, allowed_file
from config import UPLOAD_FOLDER
import pandas as pd
import io
from flask import send_file

web_admin_bp = Blueprint('web_admin', __name__)

def login_required(f):
    """Decorator untuk memastikan user sudah login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Silakan login terlebih dahulu', 'warning')
            return redirect(url_for('web_admin.web_login'))
        return f(*args, **kwargs)
    return decorated_function

@web_admin_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

# ==================== WEB LOGIN ====================

@web_admin_bp.route('/login', methods=['GET', 'POST'])
def web_login():
    """Halaman login untuk admin"""
    if 'admin_id' in session:
        return redirect(url_for('web_admin.web_dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email dan password wajib diisi', 'danger')
            return redirect(url_for('web_admin.web_login'))
        
        try:
            conn = get_db_connection()
            if not conn:
                flash('Gagal terhubung ke database', 'danger')
                return redirect(url_for('web_admin.web_login'))
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s AND is_admin = 1", (email,))
            admin = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if admin and check_password_hash(admin['password'], password):
                session['admin_id'] = admin['id']
                session['admin_name'] = admin['name']
                flash(f'Selamat datang, {admin["name"]}!', 'success')
                return redirect(url_for('web_admin.web_dashboard'))
            else:
                flash('Email atau password salah, atau Anda bukan admin', 'danger')
        except Exception as e:
            print(f"Error in web_login: {e}")
            flash('Terjadi kesalahan server', 'danger')
    
    return render_template('web_login.html')

# ==================== WEB LOGOUT ====================

@web_admin_bp.route('/logout')
def web_logout():
    """Logout dari admin"""
    session.clear()
    flash('Anda berhasil logout', 'success')
    return redirect(url_for('web_admin.web_login'))

# ==================== WEB DASHBOARD ====================

@web_admin_bp.route('/dashboard')
@login_required
def web_dashboard():
    """Dashboard utama - menampilkan statistik"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_login'))
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = 0")
        row = cursor.fetchone()
        total_users = row['count'] if row else 0
        
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = 1")
        row = cursor.fetchone()
        total_admin = row['count'] if row else 0
        
        cursor.execute("SELECT (SELECT COUNT(*) FROM face_analyses) + (SELECT COUNT(*) FROM body_analyses) as count")
        row = cursor.fetchone()
        total_records = row['count'] if row else 0
        
        cursor.execute("SELECT COUNT(*) as count FROM articles")
        row = cursor.fetchone()
        total_articles = row['count'] if row else 0
        
        cursor.execute("SELECT COUNT(*) as count FROM products")
        row = cursor.fetchone()
        total_products = row['count'] if row else 0
        
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE is_admin = 0 ORDER BY created_at DESC LIMIT 5")
        recent_users = cursor.fetchall()

        # Face analysis stats
        cursor.execute("SELECT skin_type, COUNT(*) as count FROM face_analyses GROUP BY skin_type")
        face_type_stats = cursor.fetchall()

        cursor.execute("SELECT skin_problem, COUNT(*) as count FROM face_analyses GROUP BY skin_problem")
        face_problem_stats = cursor.fetchall()

        # Body analysis stats
        cursor.execute("SELECT disease_name, COUNT(*) as count FROM body_analyses GROUP BY disease_name")
        body_disease_stats = cursor.fetchall()

        # Pending comments for classification
        cursor.execute("SELECT COUNT(*) as count FROM product_comments WHERE sentiment IS NULL")
        pending_comments = cursor.fetchone()['count']

        # Sentiment stats for comments
        cursor.execute("SELECT sentiment, COUNT(*) as count FROM product_comments WHERE sentiment IS NOT NULL GROUP BY sentiment")
        sentiment_stats = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('web_dashboard.html', 
                             total_users=total_users,
                             total_admin=total_admin,
                             total_records=total_records,
                             total_articles=total_articles,
                             total_products=total_products,
                             recent_users=recent_users,
                             face_type_stats=face_type_stats,
                             face_problem_stats=face_problem_stats,
                             body_disease_stats=body_disease_stats,
                             pending_comments=pending_comments,
                             sentiment_stats=sentiment_stats)
    except Exception as e:
        print(f"Error in web_dashboard: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_login'))
    
# ==================== WEB USERS ====================

@web_admin_bp.route('/users')
@login_required
def web_users():
    """Halaman manajemen users"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_dashboard'))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, is_admin, created_at FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('web_users.html', users=users)
    except Exception as e:
        print(f"Error in web_users: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_dashboard'))

@web_admin_bp.route('/users/<int:user_id>')
@login_required
def web_user_detail(user_id):
    """Halaman detail user"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_users'))
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = %s AND is_admin = 0", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            flash('User tidak ditemukan', 'warning')
            return redirect(url_for('web_admin.web_users'))
        
        cursor.execute("""
            SELECT 'face' as type, id, skin_problem as skin_condition, NULL as severity, notes, created_at 
            FROM face_analyses 
            WHERE user_id = %s 
            UNION ALL
            SELECT 'body' as type, id, disease_name as skin_condition, NULL as severity, notes, timestamp as created_at
            FROM body_analyses
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id, user_id))
        skin_records = cursor.fetchall()
        
        cursor.execute("""
            SELECT id, log_date, skin_load_score, status, main_triggers
            FROM daily_skin_analysis 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (user_id,))
        skin_analysis = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('web_user_detail.html', user=user, skin_records=skin_records, skin_analysis=skin_analysis)
    except Exception as e:
        print(f"Error in web_user_detail: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_users'))

@web_admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def web_delete_user(user_id):
    """Hapus user"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_users'))
        
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM face_analyses WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM body_analyses WHERE user_id = %s", (user_id,))
        
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash(f'User berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_users'))
    except Exception as e:
        print(f"Error in web_delete_user: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_users'))

@web_admin_bp.route('/users/bulk-delete', methods=['POST'])
@login_required
def web_bulk_delete_users():
    """Bulk hapus users dari admin dashboard"""
    try:
        user_ids = request.form.getlist('user_ids')

        if not user_ids:
            flash('Tidak ada user yang dipilih', 'warning')
            return redirect(url_for('web_admin.web_users'))

        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_users'))

        cursor = conn.cursor()

        # Delete related analyses first (though face_analyses has CASCADE, body_analyses might not)
        placeholders = ','.join(['%s'] * len(user_ids))
        cursor.execute(f"DELETE FROM face_analyses WHERE user_id IN ({placeholders})", user_ids)
        cursor.execute(f"DELETE FROM body_analyses WHERE user_id IN ({placeholders})", user_ids)

        # Then delete users
        cursor.execute(f"DELETE FROM users WHERE id IN ({placeholders})", user_ids)
        deleted_count = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        flash(f'{deleted_count} user berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_users'))
    except Exception as e:
        print(f"Error in web_bulk_delete_users: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_users'))

# ==================== WEB ARTICLES ====================

@web_admin_bp.route('/articles')
@login_required
def web_articles():
    """Halaman manajemen artikel"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_dashboard'))

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, title, description, image, created_at FROM articles ORDER BY created_at DESC")
        articles = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('web_articles.html', articles=articles)
    except Exception as e:
        print(f"Error in web_articles: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_dashboard'))


@web_admin_bp.route('/articles/create', methods=['GET', 'POST'])
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
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                image_filename = filename

        if not title or not description:
            flash('Title dan description wajib diisi', 'danger')
            return redirect(url_for('web_admin.web_create_article'))

        try:
            conn = get_db_connection()
            if not conn:
                flash('Gagal terhubung ke database', 'danger')
                return redirect(url_for('web_admin.web_articles'))

            cursor = conn.cursor()
            cursor.execute("INSERT INTO articles (title, description, image) VALUES (%s, %s, %s)", (title, description, image_filename))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Artikel berhasil dibuat', 'success')
            return redirect(url_for('web_admin.web_articles'))
        except Exception as e:
            print(f"Error in web_create_article: {e}")
            flash('Terjadi kesalahan server', 'danger')
            return redirect(url_for('web_admin.web_articles'))

    return render_template('web_article_form.html', article=None)


@web_admin_bp.route('/articles/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def web_edit_article(article_id):
    """Edit artikel melalui admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_articles'))

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
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
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
                return redirect(url_for('web_admin.web_edit_article', article_id=article_id))

            cursor.execute("UPDATE articles SET title = %s, description = %s, image = %s WHERE id = %s", (title, description, image_filename, article_id))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Artikel berhasil diperbarui', 'success')
            return redirect(url_for('web_admin.web_articles'))

        cursor.execute("SELECT id, title, description, image, created_at FROM articles WHERE id = %s", (article_id,))
        article = cursor.fetchone()

        cursor.close()
        conn.close()

        if not article:
            flash('Artikel tidak ditemukan', 'warning')
            return redirect(url_for('web_admin.web_articles'))

        return render_template('web_article_form.html', article=article)
    except Exception as e:
        print(f"Error in web_edit_article: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_articles'))


@web_admin_bp.route('/articles/<int:article_id>/delete', methods=['POST'])
@login_required
def web_delete_article(article_id):
    """Hapus artikel dari admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_articles'))

        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = %s", (article_id,))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Artikel berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_articles'))
    except Exception as e:
        print(f"Error in web_delete_article: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_articles'))

@web_admin_bp.route('/articles/bulk-delete', methods=['POST'])
@login_required
def web_bulk_delete_articles():
    """Bulk hapus articles dari admin dashboard"""
    try:
        article_ids = request.form.getlist('article_ids')

        if not article_ids:
            flash('Tidak ada artikel yang dipilih', 'warning')
            return redirect(url_for('web_admin.web_articles'))

        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_articles'))

        cursor = conn.cursor()

        # Create placeholders for the IN clause
        placeholders = ','.join(['%s'] * len(article_ids))
        cursor.execute(f"DELETE FROM articles WHERE id IN ({placeholders})", article_ids)
        deleted_count = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        flash(f'{deleted_count} artikel berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_articles'))
    except Exception as e:
        print(f"Error in web_bulk_delete_articles: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_articles'))

# ==================== WEB PRODUCTS ====================
    
@web_admin_bp.route('/products')
@login_required
def web_products():
    """Halaman manajemen product"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_dashboard'))

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi FROM products ORDER BY id DESC")
        products = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('web_products.html', products=products)
    except Exception as e:
        print(f"Error in web_products: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_dashboard'))


@web_admin_bp.route('/products/create', methods=['GET', 'POST'])
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
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                image_filename = filename

        if not merek or not nama or not harga or not kategori_penyakit:
            flash('Merek, nama, harga, dan kategori penyakit wajib diisi', 'danger')
            return redirect(url_for('web_admin.web_create_product'))

        try:
            conn = get_db_connection()
            if not conn:
                flash('Gagal terhubung ke database', 'danger')
                return redirect(url_for('web_admin.web_products'))

            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (merek, nama, harga, kategori_penyakit, image_filename, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Produk berhasil dibuat', 'success')
            return redirect(url_for('web_admin.web_products'))
        except Exception as e:
            print(f"Error in web_create_product: {e}")
            flash('Terjadi kesalahan server', 'danger')
            return redirect(url_for('web_admin.web_products'))

    return render_template('web_product_form.html', product=None)

@web_admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def web_edit_product(product_id):
    """Edit product melalui admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_products'))

        cursor = conn.cursor(dictionary=True, buffered=True)
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
            
            # Ambil gambar lama dari DB sebagai default
            cursor.execute("SELECT image FROM products WHERE id = %s", (product_id,))
            current = cursor.fetchone()
            image_filename = current['image'] if current else None

            image_url = request.form.get('image_url', '').strip()
            if image_url:
                image_filename = image_url

            elif 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    image_filename = filename

            if not merek or not nama or not harga or not kategori_penyakit:
                flash('Merek, nama, harga, dan kategori penyakit wajib diisi', 'danger')
                cursor.close()
                conn.close()
                return redirect(url_for('web_admin.web_edit_product', product_id=product_id))

            cursor.execute("UPDATE products SET merek = %s, nama = %s, harga = %s, kategori_penyakit = %s, image = %s, deskripsi = %s, dosis = %s, efek_samping = %s, komposisi = %s, manufaktur = %s, nomor_registrasi = %s WHERE id = %s", (merek, nama, harga, kategori_penyakit, image_filename, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi, product_id))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Produk berhasil diperbarui', 'success')
            return redirect(url_for('web_admin.web_products'))

        cursor.execute("SELECT id, merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()

        cursor.close()
        conn.close()

        if not product:
            flash('Produk tidak ditemukan', 'warning')
            return redirect(url_for('web_admin.web_products'))

        return render_template('web_product_form.html', product=product)
    except Exception as e:
        import traceback
        print(f"Error in web_edit_product: {e}")
        traceback.print_exc()
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_products'))


@web_admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
def web_delete_product(product_id):
    """Hapus product dari admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_products'))

        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Produk berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_products'))
    except Exception as e:
        print(f"Error in web_delete_article: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_products'))

@web_admin_bp.route('/products/bulk-delete', methods=['POST'])
@login_required
def web_bulk_delete_products():
    """Bulk hapus products dari admin dashboard"""
    try:
        product_ids = request.form.getlist('product_ids')

        if not product_ids:
            flash('Tidak ada produk yang dipilih', 'warning')
            return redirect(url_for('web_admin.web_products'))

        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_products'))

        cursor = conn.cursor()

        # Create placeholders for the IN clause
        placeholders = ','.join(['%s'] * len(product_ids))
        cursor.execute(f"DELETE FROM products WHERE id IN ({placeholders})", product_ids)
        deleted_count = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        flash(f'{deleted_count} produk berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_products'))
    except Exception as e:
        print(f"Error in web_bulk_delete_products: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_products'))

@web_admin_bp.route('/products/import/template')
@login_required
def web_download_product_template():
    cols = [
        'merek', 'nama', 'harga', 'kategori_penyakit',
        'image',  # OPSIONAL
        'deskripsi', 'dosis', 'efek_samping',
        'komposisi', 'manufaktur', 'nomor_registrasi'
    ]

    df = pd.DataFrame(columns=cols)

    df.loc[0] = {
        'merek': 'Brand ABC',
        'nama': 'Serum Vitamin C',
        'harga': 150000,
        'kategori_penyakit': 'Acne',
        'image': '',  # boleh dikosongkan
        'deskripsi': 'Deskripsi produk...',
        'dosis': '2x sehari',
        'efek_samping': 'Kemerahan ringan',
        'komposisi': 'Aqua, Vit C, Glycerin',
        'manufaktur': 'PT. Farmasi',
        'nomor_registrasi': 'NA123456789'
    }

    output = io.BytesIO()
    df.to_csv(output, index=False, sep=';')
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='template_produk.csv'
    )


@web_admin_bp.route('/products/import', methods=['POST'])
@login_required
def web_import_products():
    """Import produk dari file CSV atau Excel"""
    if 'file' not in request.files:
        flash('Tidak ada file yang diunggah', 'danger')
        return redirect(url_for('web_admin.web_products'))
        
    file = request.files['file']
    if file.filename == '':
        flash('Nama file kosong', 'danger')
        return redirect(url_for('web_admin.web_products'))
        
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)

            df.columns = df.columns.str.strip().str.replace('\xa0', '')
            print("COLUMNS:", df.columns.tolist())

        else:
            flash('Format file tidak didukung. Gunakan CSV atau Excel', 'danger')
            return redirect(url_for('web_admin.web_products'))
            
        required_cols = ['merek', 'nama', 'harga', 'kategori_penyakit']
        for col in required_cols:
            if col not in df.columns:
                flash(f'Kolom wajib "{col}" tidak ditemukan dalam file', 'danger')
                return redirect(url_for('web_admin.web_products'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        count = 0
        for _, row in df.iterrows():
            image = None

            if 'gambar' in df.columns and not pd.isna(row['gambar']):
                image = unquote(str(row['gambar']).strip())

            print("IMAGE FROM EXCEL:", repr(image))

            if pd.isna(row['merek']) or pd.isna(row['nama']):
                continue
                
            cursor.execute("""
                INSERT INTO products 
                (merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(row['merek']),
                str(row['nama']),
                row['harga'] if not pd.isna(row['harga']) else 0,
                str(row['kategori_penyakit']) if not pd.isna(row['kategori_penyakit']) else None,
                image,
                str(row['deskripsi']) if 'deskripsi' in df.columns and not pd.isna(row['deskripsi']) else None,
                str(row['dosis']) if 'dosis' in df.columns and not pd.isna(row['dosis']) else None,
                str(row['efek_samping']) if 'efek_samping' in df.columns and not pd.isna(row['efek_samping']) else None,
                str(row['komposisi']) if 'komposisi' in df.columns and not pd.isna(row['komposisi']) else None,
                str(row['manufaktur']) if 'manufaktur' in df.columns and not pd.isna(row['manufaktur']) else None,
                str(row['nomor_registrasi']) if 'nomor_registrasi' in df.columns and not pd.isna(row['nomor_registrasi']) else None
            ))
            count += 1
            
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f'Berhasil mengimpor {count} produk', 'success')
    except Exception as e:
        print(f"Error in web_import_products: {e}")
        flash(f'Terjadi kesalahan saat mengimpor data: {str(e)}', 'danger')
        
    return redirect(url_for('web_admin.web_products'))

# ==================== WEB FOODS ====================
    
@web_admin_bp.route('/foods-and-drinks')
@login_required
def web_foods_and_drinks():
    """Halaman manajemen makanan dan minuman"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_dashboard'))

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, oil, simple_carb, sugar, fiber, fermented FROM foods ORDER BY id DESC")
        foods = cursor.fetchall()
        
        cursor.execute("SELECT id, name, drink_type, sugar FROM drinks ORDER BY id DESC")
        drinks = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('web_foods_and_drinks.html', foods=foods, drinks=drinks)
    except Exception as e:
        print(f"Error in web_foods_and_drinks: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_dashboard'))


@web_admin_bp.route('/foods/create', methods=['GET', 'POST'])
@login_required
def web_create_food():
    """Buat food baru melalui admin dashboard"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        oil = request.form.get('oil', '').strip()
        simple_carb = request.form.get('simple_carb', '').strip()
        sugar = request.form.get('sugar', '').strip()
        fiber = request.form.get('fiber', '').strip()
        fermented = request.form.get('fermented', '').strip()

        if not name or not oil or not simple_carb or not sugar or not fiber or not fermented:
            flash('Nama, oil, simple_carb, sugar, fiber, dan fermented wajib diisi', 'danger')
            return redirect(url_for('web_admin.web_create_food'))

        try:
            conn = get_db_connection()
            if not conn:
                flash('Gagal terhubung ke database', 'danger')
                return redirect(url_for('web_admin.web_foods_and_drinks'))

            cursor = conn.cursor()
            cursor.execute("INSERT INTO foods (name, oil, simple_carb, sugar, fiber, fermented) VALUES (%s, %s, %s, %s, %s, %s)", (name, oil, simple_carb, sugar, fiber, fermented))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Makanan berhasil dibuat', 'success')
            return redirect(url_for('web_admin.web_foods_and_drinks'))
        except Exception as e:
            print(f"Error in web_create_food: {e}")
            flash('Terjadi kesalahan server', 'danger')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

    return render_template('web_food_form.html', food=None)

@web_admin_bp.route('/foods/<int:food_id>/edit', methods=['GET', 'POST'])
@login_required
def web_edit_food(food_id):
    """Edit food melalui admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            oil = request.form.get('oil', '').strip()
            simple_carb = request.form.get('simple_carb', '').strip()
            sugar = request.form.get('sugar', '').strip()
            fiber = request.form.get('fiber', '').strip()
            fermented = request.form.get('fermented', '').strip()

            if not name or not oil or not simple_carb or not sugar or not fiber or not fermented:
                flash('Nama, oil, simple_carb, sugar, fiber, dan fermented wajib diisi', 'danger')
                cursor.close()
                conn.close()
                return redirect(url_for('web_admin.web_edit_food', food_id=food_id))

            cursor.execute("UPDATE foods SET name = %s, oil = %s, simple_carb = %s, sugar = %s, fiber = %s, fermented = %s WHERE id = %s", (name, oil, simple_carb, sugar, fiber, fermented, food_id))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Makanan berhasil diperbarui', 'success')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        cursor.execute("SELECT id, name, oil, simple_carb, sugar, fiber, fermented FROM foods WHERE id = %s", (food_id,))
        food = cursor.fetchone()

        cursor.close()
        conn.close()

        if not food:
            flash('Makanan tidak ditemukan', 'warning')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        return render_template('web_food_form.html', food=food)
    except Exception as e:
        print(f"Error in web_edit_food: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_foods_and_drinks'))


@web_admin_bp.route('/foods/<int:food_id>/delete', methods=['POST'])
@login_required
def web_delete_food(food_id):
    """Hapus food dari admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        cursor = conn.cursor()
        cursor.execute("DELETE FROM foods WHERE id = %s", (food_id,))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Makanan berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_foods_and_drinks'))
    except Exception as e:
        print(f"Error in web_delete_food: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_foods_and_drinks'))

@web_admin_bp.route('/foods/bulk-delete', methods=['POST'])
@login_required
def web_bulk_delete_foods():
    """Bulk hapus foods dari admin dashboard"""
    try:
        food_ids = request.form.getlist('food_ids')

        if not food_ids:
            flash('Tidak ada makanan yang dipilih', 'warning')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        cursor = conn.cursor()

        # Create placeholders for the IN clause
        placeholders = ','.join(['%s'] * len(food_ids))
        cursor.execute(f"DELETE FROM foods WHERE id IN ({placeholders})", food_ids)
        deleted_count = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        flash(f'{deleted_count} makanan berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_foods_and_drinks'))
    except Exception as e:
        print(f"Error in web_bulk_delete_foods: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_foods_and_drinks'))

@web_admin_bp.route('/drinks/create', methods=['GET', 'POST'])
@login_required
def web_create_drink():
    """Buat minuman baru melalui admin dashboard"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        drink_type = request.form.get('drink_type', '').strip()
        sugar = request.form.get('sugar', '').strip()

        if not name or not drink_type or not sugar:
            flash('Nama, jenis minuman, dan gula wajib diisi', 'danger')
            return redirect(url_for('web_admin.web_create_drink'))

        try:
            conn = get_db_connection()
            if not conn:
                flash('Gagal terhubung ke database', 'danger')
                return redirect(url_for('web_admin.web_foods_and_drinks'))

            cursor = conn.cursor()
            cursor.execute("INSERT INTO drinks (name, drink_type, sugar) VALUES (%s, %s, %s)", (name, drink_type, sugar))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Minuman berhasil dibuat', 'success')
            return redirect(url_for('web_admin.web_foods_and_drinks'))
        except Exception as e:
            print(f"Error in web_create_drink: {e}")
            flash('Terjadi kesalahan server', 'danger')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

    return render_template('web_drink_form.html', drink=None)

@web_admin_bp.route('/drinks/<int:drink_id>/edit', methods=['GET', 'POST'])
@login_required
def web_edit_drink(drink_id):
    """Edit minuman melalui admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            drink_type = request.form.get('drink_type', '').strip()
            sugar = request.form.get('sugar', '').strip()
            
            if not name or not drink_type or not sugar:
                flash('Nama, jenis minuman, dan gula wajib diisi', 'danger')
                cursor.close()
                conn.close()
                return redirect(url_for('web_admin.web_edit_drink', drink_id=drink_id)) 

            cursor.execute("UPDATE drinks SET name = %s, drink_type = %s, sugar = %s WHERE id = %s", (name, drink_type, sugar, drink_id))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Minuman berhasil diperbarui', 'success')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        cursor.execute("SELECT id, name, drink_type, sugar FROM drinks WHERE id = %s", (drink_id,))
        drink = cursor.fetchone()

        cursor.close()
        conn.close()

        if not drink:
            flash('Minuman tidak ditemukan', 'warning')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        return render_template('web_drink_form.html', drink=drink)
    except Exception as e:
        print(f"Error in web_edit_drink: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_foods_and_drinks'))


@web_admin_bp.route('/drinks/<int:drink_id>/delete', methods=['POST'])
@login_required
def web_delete_drink(drink_id):
    """Hapus minuman dari admin dashboard"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        cursor = conn.cursor()
        cursor.execute("DELETE FROM drinks WHERE id = %s", (drink_id,))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Minuman berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_foods_and_drinks'))
    except Exception as e:
        print(f"Error in web_delete_drink: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_foods_and_drinks'))

@web_admin_bp.route('/drinks/bulk-delete', methods=['POST'])
@login_required
def web_bulk_delete_drinks():
    """Bulk hapus minuman dari admin dashboard"""
    try:
        drink_ids = request.form.getlist('drink_ids')

        if not drink_ids:
            flash('Tidak ada minuman yang dipilih', 'warning')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_foods_and_drinks'))

        cursor = conn.cursor()

        # Create placeholders for the IN clause
        placeholders = ','.join(['%s'] * len(drink_ids))
        cursor.execute(f"DELETE FROM drinks WHERE id IN ({placeholders})", drink_ids)
        deleted_count = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        flash(f'{deleted_count} minuman berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_foods_and_drinks'))
    except Exception as e:
        print(f"Error in web_bulk_delete_drinks: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_foods_and_drinks'))

@web_admin_bp.route('/foods-and-drinks/import/template')
@login_required
def web_download_food_template():
    """Download template CSV untuk import makanan/minuman"""
    target = request.args.get('target', 'foods')
    
    if target == 'drinks':
        cols = ['name', 'drink_type', 'sugar']
        df = pd.DataFrame(columns=cols)
        df.loc[0] = {'name': 'Teh Manis', 'drink_type': 'SWEET', 'sugar': 3}
        filename = 'template_minuman.csv'
    else:
        cols = ['name', 'oil', 'simple_carb', 'sugar', 'fiber', 'fermented']
        df = pd.DataFrame(columns=cols)
        df.loc[0] = {'name': 'Nasi Goreng', 'oil': 3, 'simple_carb': 4, 'sugar': 1, 'fiber': 0, 'fermented': 0}
        filename = 'template_makanan.csv'
    
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name=filename)

@web_admin_bp.route('/foods-and-drinks/import', methods=['POST'])
@login_required
def web_import_foods_drinks():
    """Import makanan atau minuman dari file CSV atau Excel"""
    target = request.form.get('target', 'foods')
    if 'file' not in request.files:
        flash('Tidak ada file yang diunggah', 'danger')
        return redirect(url_for('web_admin.web_foods_and_drinks'))
        
    file = request.files['file']
    if file.filename == '':
        flash('Nama file kosong', 'danger')
        return redirect(url_for('web_admin.web_foods_and_drinks'))
        
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            flash('Format file tidak didukung', 'danger')
            return redirect(url_for('web_admin.web_foods_and_drinks'))
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        count = 0
        if target == 'drinks':
            required_cols = ['name', 'drink_type', 'sugar']
            for col in required_cols:
                if col not in df.columns:
                    flash(f'Kolom wajib "{col}" tidak ditemukan', 'danger')
                    return redirect(url_for('web_admin.web_foods_and_drinks'))
            
            for _, row in df.iterrows():
                if pd.isna(row['name']) or pd.isna(row['drink_type']):
                    continue
                cursor.execute("INSERT INTO drinks (name, drink_type, sugar) VALUES (%s, %s, %s)", (str(row['name']), str(row['drink_type']), int(row['sugar']) if not pd.isna(row['sugar']) else 0))
                count += 1
        else:
            required_cols = ['name', 'oil', 'simple_carb', 'sugar', 'fiber', 'fermented']
            for col in required_cols:
                if col not in df.columns:
                    flash(f'Kolom wajib "{col}" tidak ditemukan', 'danger')
                    return redirect(url_for('web_admin.web_foods_and_drinks'))
            
            for _, row in df.iterrows():
                if pd.isna(row['name']):
                    continue
                cursor.execute("INSERT INTO foods (name, oil, simple_carb, sugar, fiber, fermented) VALUES (%s, %s, %s, %s, %s, %s)", (
                    str(row['name']), 
                    int(row['oil']) if not pd.isna(row['oil']) else 0,
                    int(row['simple_carb']) if not pd.isna(row['simple_carb']) else 0,
                    int(row['sugar']) if not pd.isna(row['sugar']) else 0,
                    int(row['fiber']) if not pd.isna(row['fiber']) else 0,
                    int(row['fermented']) if not pd.isna(row['fermented']) else 0
                ))
                count += 1
            
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f'Berhasil mengimpor {count} item', 'success')
    except Exception as e:
        print(f"Error in web_import_foods_drinks: {e}")
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        
    return redirect(url_for('web_admin.web_foods_and_drinks'))

# ==================== WEB SKIN DATA ====================

@web_admin_bp.route('/skin-data')
@login_required
def web_skin_data():
    """Halaman manajemen data kulit"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_dashboard'))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 'face' as type, CAST(fa.id AS CHAR) as id, fa.user_id, fa.skin_problem as skin_condition, NULL as severity, fa.notes, fa.created_at, u.name
            FROM face_analyses fa
            JOIN users u ON fa.user_id = u.id
            UNION ALL
            SELECT 'body' as type, CAST(ba.id AS CHAR) as id, ba.user_id, ba.disease_name as skin_condition, NULL as severity, ba.notes, ba.timestamp as created_at, u.name
            FROM body_analyses ba
            JOIN users u ON ba.user_id = u.id
            ORDER BY created_at DESC
        """)
        skin_data = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('web_skin_data.html', skin_data=skin_data)
    except Exception as e:
        print(f"Error in web_skin_data: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_dashboard'))

@web_admin_bp.route('/skin-data/<string:record_id>/delete', methods=['POST'])
@login_required
def web_delete_skin_record(record_id):
    """Hapus record kulit (face_analyses atau body_analyses)"""
    try:
        table_type = request.args.get('type', 'face')
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_skin_data'))
        
        cursor = conn.cursor()
        if table_type == 'body':
            cursor.execute("DELETE FROM body_analyses WHERE id = %s", (record_id,))
        else:
            cursor.execute("DELETE FROM face_analyses WHERE id = %s", (record_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash(f'Record {table_type} berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_skin_data'))
    except Exception as e:
        print(f"Error in web_delete_skin_record: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_skin_data'))
    
@web_admin_bp.route('/skin-records/bulk-delete', methods=['POST'])
@login_required
def web_bulk_delete_skin_records():
    """Bulk hapus skin records dari admin dashboard"""
    try:
        record_identifiers = request.form.getlist('record_ids') # Expected format: "face:UUID" or "body:UUID"

        if not record_identifiers:
            flash('Tidak ada record yang dipilih', 'warning')
            return redirect(url_for('web_admin.web_skin_data'))

        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_skin_data'))

        cursor = conn.cursor()

        face_ids = [ri.split(':')[1] for ri in record_identifiers if ri.startswith('face:') and ':' in ri]
        body_ids = [ri.split(':')[1] for ri in record_identifiers if ri.startswith('body:') and ':' in ri]
        
        deleted_count = 0
        if face_ids:
            placeholders = ','.join(['%s'] * len(face_ids))
            cursor.execute(f"DELETE FROM face_analyses WHERE id IN ({placeholders})", face_ids)
            deleted_count += cursor.rowcount
            
        if body_ids:
            placeholders = ','.join(['%s'] * len(body_ids))
            cursor.execute(f"DELETE FROM body_analyses WHERE id IN ({placeholders})", body_ids)
            deleted_count += cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        flash(f'{deleted_count} record berhasil dihapus', 'success')
        return redirect(url_for('web_admin.web_skin_data'))
    except Exception as e:
        print(f"Error in web_bulk_delete_skin_records: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_skin_data'))
    
# ==================== WEB SETTINGS ====================

@web_admin_bp.route('/settings')
@login_required
def web_settings():
    """Halaman pengaturan"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_dashboard'))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (session.get('admin_id'),))
        admin = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('web_settings.html', admin=admin)
    except Exception as e:
        print(f"Error in web_settings: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_dashboard'))

@web_admin_bp.route('/settings/update-password', methods=['POST'])
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
            return redirect(url_for('web_admin.web_settings'))
        
        if new_password != confirm_password:
            flash('Password baru tidak cocok', 'danger')
            return redirect(url_for('web_admin.web_settings'))
        
        if len(new_password) < 6:
            flash('Password minimal 6 karakter', 'danger')
            return redirect(url_for('web_admin.web_settings'))
        
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_settings'))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password FROM users WHERE id = %s", (admin_id,))
        admin = cursor.fetchone()
        
        if not admin or not check_password_hash(admin['password'], old_password):
            flash('Password lama salah', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('web_admin.web_settings'))
        
        hashed_password = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, admin_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Password berhasil diubah', 'success')
        return redirect(url_for('web_admin.web_settings'))
    except Exception as e:
        print(f"Error in web_update_password: {e}")
        flash('Terjadi kesalahan server', 'danger')
        return redirect(url_for('web_admin.web_settings'))