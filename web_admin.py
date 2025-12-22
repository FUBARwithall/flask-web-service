from flask import Blueprint, request, render_template, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
import os
from models import get_db_connection, allowed_file
from config import UPLOAD_FOLDER

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
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE is_admin = 0 ORDER BY created_at DESC")
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
        
        cursor.execute("DELETE FROM skin_data WHERE user_id = %s", (user_id,))
        
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
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
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
        print(f"Error in web_edit_product: {e}")
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
        return redirect(url_for('web_admin.web_dashboard'))

@web_admin_bp.route('/skin-data/<int:record_id>/delete', methods=['POST'])
@login_required
def web_delete_skin_record(record_id):
    """Hapus record kulit"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_skin_data'))
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM skin_data WHERE id = %s", (record_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Record kulit berhasil dihapus', 'success')
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
        record_ids = request.form.getlist('record_ids')

        if not record_ids:
            flash('Tidak ada record yang dipilih', 'warning')
            return redirect(url_for('web_admin.web_skin_data'))

        conn = get_db_connection()
        if not conn:
            flash('Gagal terhubung ke database', 'danger')
            return redirect(url_for('web_admin.web_skin_data'))

        cursor = conn.cursor()

        # Delete skin records
        placeholders = ','.join(['%s'] * len(record_ids))
        cursor.execute(f"DELETE FROM skin_data WHERE id IN ({placeholders})", record_ids)
        deleted_count = cursor.rowcount

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