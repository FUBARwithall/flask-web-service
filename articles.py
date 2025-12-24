from flask import Blueprint, request, jsonify
from models import get_db_connection

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/api/articles', methods=['GET'])
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


@articles_bp.route('/api/articles/<int:article_id>', methods=['GET'])
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

# ==================== ARTICLES FAVORITE ====================

@articles_bp.route('/api/articles/<int:article_id>/favorite', methods=['POST'])
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


@articles_bp.route('/api/articles/<int:article_id>/favorite', methods=['DELETE'])
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


@articles_bp.route('/api/articles/<int:article_id>/favorite/status', methods=['GET'])
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


@articles_bp.route('/api/articles/favorites', methods=['GET'])
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