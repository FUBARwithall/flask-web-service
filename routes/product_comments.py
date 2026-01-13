from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_db_connection

product_comments_bp = Blueprint('product_comments', __name__)


@product_comments_bp.route('/api/products/<int:product_id>/comments', methods=['GET'])
def get_comments(product_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Gagal terhubung ke database'}), 500
        
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                c.id,
                c.user_id,
                u.name AS user_name,
                c.comment,
                c.created_at
            FROM product_comments c
            JOIN users u ON u.id = c.user_id
            WHERE c.product_id = %s
            ORDER BY c.created_at DESC
        """, (product_id,))

        comments = cursor.fetchall()
        cursor.close()
        conn.close()

        for c in comments:
            if c['created_at']:
                c['created_at'] = c['created_at'].strftime('%Y-%m-%d %H:%M')

        return jsonify({'success': True, 'data': comments}), 200
    except Exception as e:
        print(f"Error getting comments: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500

@product_comments_bp.route('/api/products/<int:product_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(product_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        comment = data.get('comment')

        if not comment:
            return jsonify({'success': False, 'message': 'Komentar tidak boleh kosong'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Gagal terhubung ke database'}), 500
        
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO product_comments (product_id, user_id, comment)
            VALUES (%s, %s, %s)
        """, (product_id, user_id, comment))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Komentar berhasil ditambahkan'}), 201
    except Exception as e:
        print(f"Error adding comment: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500
    
@product_comments_bp.route('/api/products/<int:product_id>/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(product_id, comment_id):
    try:
        user_id = int(get_jwt_identity())  # Convert to int

        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Gagal terhubung ke database'}), 500
        
        cursor = conn.cursor(dictionary=True)

        # Check if comment exists and user is the owner
        cursor.execute("""
            SELECT user_id FROM product_comments
            WHERE id = %s AND product_id = %s
        """, (comment_id, product_id))
        
        comment = cursor.fetchone()
        
        if not comment:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Komentar tidak ditemukan'}), 404
        
        # Only allow user who created the comment to delete it
        if comment['user_id'] != user_id:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Anda hanya bisa menghapus komentar sendiri'}), 403
        
        # Delete the comment
        cursor.execute("""
            DELETE FROM product_comments
            WHERE id = %s
        """, (comment_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Komentar berhasil dihapus'}), 200
    except Exception as e:
        print(f"Error deleting comment: {e}")
        return jsonify({'success': False, 'message': 'Terjadi kesalahan server'}), 500