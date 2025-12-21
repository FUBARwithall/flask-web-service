from flask import Blueprint, request, jsonify
from models import get_db_connection

products_bp = Blueprint('products', __name__)

@products_bp.route('/api/products', methods=['GET'])
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


@products_bp.route('/api/products/<int:product_id>', methods=['GET'])
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


@products_bp.route('/api/products', methods=['POST'])
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


@products_bp.route('/api/products/<int:product_id>', methods=['PUT'])
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


@products_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
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

# ==================== PRODUCTS FAVORITE ====================

@products_bp.route('/api/products/<int:product_id>/favorite', methods=['POST'])
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


@products_bp.route('/api/products/<int:product_id>/favorite', methods=['DELETE'])
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


@products_bp.route('/api/products/<int:product_id>/favorite/status', methods=['GET'])
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


@products_bp.route('/api/products/favorites', methods=['GET'])
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