from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_db_connection

products_bp = Blueprint('products', __name__)

@products_bp.route('/api/products', methods=['GET'])
@jwt_required()
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

        # Convert Decimal to float for JSON serialization
        for p in products:
            if p.get('harga'):
                p['harga'] = float(p['harga'])

        return jsonify({'status': 'success', 'data': products}), 200
    except Exception as e:
        print(f"Error in get_products: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500


@products_bp.route('/api/products/by-category', methods=['GET'])
@jwt_required()
def get_products_by_category():
    """Ambil products berdasarkan kategori penyakit (untuk rekomendasi deteksi)"""
    try:
        category = request.args.get('category', '').strip().lower()
        
        if not category:
            return jsonify({'status': 'error', 'message': 'Parameter category diperlukan'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)
        
        # Search for products where kategori_penyakit contains the category (case-insensitive)
        cursor.execute("""
            SELECT id, merek, nama, harga, kategori_penyakit, image, deskripsi, dosis, efek_samping, komposisi, manufaktur, nomor_registrasi 
            FROM products 
            WHERE LOWER(kategori_penyakit) LIKE %s
            ORDER BY id DESC
            LIMIT 10
        """, (f'%{category}%',))
        
        products = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert Decimal to float for JSON serialization
        for p in products:
            if p.get('harga'):
                p['harga'] = float(p['harga'])

        return jsonify({'status': 'success', 'data': products}), 200
    except Exception as e:
        print(f"Error in get_products_by_category: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500


@products_bp.route('/api/products/<int:product_id>', methods=['GET'])
@jwt_required()
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

        # Convert Decimal to float for JSON serialization
        if product.get('harga'):
            product['harga'] = float(product['harga'])

        return jsonify({'status': 'success', 'data': product}), 200
    except Exception as e:
        print(f"Error in get_product: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

# ==================== PRODUCTS FAVORITE ====================

@products_bp.route('/api/products/<int:product_id>/favorite', methods=['POST'])
@jwt_required()
def favorite_product(product_id):
    user_id = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT IGNORE INTO product_favorites (user_id, product_id)
        VALUES (%s, %s)
    """, (user_id, product_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Produk berhasil ditambahkan ke favorit'})


@products_bp.route('/api/products/<int:product_id>/favorite', methods=['DELETE'])
@jwt_required()
def unfavorite_product(product_id):
    user_id = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM product_favorites
        WHERE user_id = %s AND product_id = %s
    """, (user_id, product_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Produk berhasil dihapus dari favorit'})


@products_bp.route('/api/products/<int:product_id>/favorite/status', methods=['GET'])
@jwt_required()
def product_favorite_status(product_id):
    user_id = get_jwt_identity()

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
@jwt_required()
def get_favorite_products():
    try:
        user_id = get_jwt_identity()

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

        # Convert Decimal to float for JSON serialization
        for p in products:
            if p.get('harga'):
                p['harga'] = float(p['harga'])

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
