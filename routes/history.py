from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_db_connection
from flask import send_from_directory
import os

history_bp = Blueprint('history', __name__, url_prefix='/api/history')


# ======================================================
# DUMMY LOG EVENT (jika belum ada utils.history_logger)
# ======================================================
def log_event(user_id, event_type, analysis_id=None, metadata=None):
    """Dummy logger untuk sementara"""
    print(f"[LOG] User: {user_id}, Event: {event_type}, Analysis ID: {analysis_id}")
    pass


# ======================================================
# GET HISTORY LIST
# ======================================================
@history_bp.route('', methods=['GET'])
@jwt_required()
def get_user_history():
    user_id = get_jwt_identity()
    conn = None
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'DB connection failed'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                id,
                timestamp,
                skin_type,
                skin_problem,
                CONCAT('/api/history/images/', image_filename) AS image_url
            FROM face_analyses
            WHERE user_id = %s
            ORDER BY timestamp DESC
            LIMIT 50
        """, (user_id,))

        
        history = cursor.fetchall()
        cursor.close()

        # Log event (non-blocking)
        try:
            log_event(user_id, 'VIEW_HISTORY')
        except Exception as e:
            print(f"[WARNING] Log failed: {e}")

        return jsonify({'success': True, 'history': history}), 200

    except Exception as e:
        print(f"[ERROR] get_user_history: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    
    finally:
        if conn:
            conn.close()

@history_bp.route('/images/<filename>')
def serve_history_image(filename):
    return send_from_directory(
        'static/uploads/analyses',
        filename
    )

# ======================================================
# GET HISTORY DETAIL
# ======================================================
@history_bp.route('/<int:analysis_id>', methods=['GET'])
@jwt_required()
def get_history_detail(analysis_id):
    user_id = get_jwt_identity()
    conn = None

    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'DB connection failed'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                id,
                timestamp,
                image_filename,
                skin_type,
                skin_type_confidence,
                skin_type_predictions,
                skin_problem,
                skin_problem_confidence,
                skin_problem_predictions
            FROM face_analyses
            WHERE id = %s AND user_id = %s
        """, (analysis_id, user_id))

        row = cursor.fetchone()
        cursor.close()

        if not row:
            return jsonify({'success': False, 'message': 'Data not found'}), 404

        # 🔁 FORMAT ULANG BIAR SAMA DENGAN DETEKSI
        data = {
            'timestamp': row['timestamp'].isoformat() if row['timestamp'] else None,
            'image_url': f"/api/history/images/{row['image_filename']}"
            if row.get('image_filename') else None,

            'skin_type_analysis': {
                'result': row.get('skin_type'),
                'confidence': row.get('skin_type_confidence'),
                'all_predictions': row.get('skin_type_predictions') or {}
            },

            'skin_problem_analysis': {
                'result': row.get('skin_problem'),
                'confidence': row.get('skin_problem_confidence'),
                'all_predictions': row.get('skin_problem_predictions') or {}
            }
        }

        try:
            log_event(user_id, 'VIEW_DETAIL', analysis_id)
        except Exception as e:
            print(f"[WARNING] Log failed: {e}")

        return jsonify({
            'success': True,
            'data': data
        }), 200

    except Exception as e:
        print(f"[ERROR] get_history_detail: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

    finally:
        if conn:
            conn.close()




# ======================================================
# DELETE HISTORY (HARD DELETE)
# ======================================================
@history_bp.route('/<int:analysis_id>', methods=['DELETE'])
@jwt_required()
def delete_history(analysis_id):
    user_id = get_jwt_identity()
    conn = None
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'DB connection failed'}), 500

        cursor = conn.cursor(dictionary=True)

        # Ambil file gambar dulu
        cursor.execute("""
            SELECT image_filename
            FROM face_analyses
            WHERE id = %s AND user_id = %s
        """, (analysis_id, user_id))
        row = cursor.fetchone()

        if not row:
            cursor.close()
            return jsonify({'success': False, 'message': 'Data not found'}), 404

        # Hapus data DB
        cursor.execute("""
            DELETE FROM face_analyses
            WHERE id = %s AND user_id = %s
        """, (analysis_id, user_id))

        conn.commit()
        cursor.close()

        # Hapus file gambar (optional, dengan error handling)
        if row.get('image_filename'):
            try:
                image_path = os.path.join('static/uploads/analyses', row['image_filename'])
                if os.path.exists(image_path):
                    os.remove(image_path)
                    print(f"[INFO] Deleted image: {image_path}")
            except Exception as e:
                print(f"[WARNING] Failed to delete image: {e}")

        # Log event
        try:
            log_event(user_id, 'DELETE', analysis_id)
        except Exception as e:
            print(f"[WARNING] Log failed: {e}")

        return jsonify({'success': True, 'message': 'History deleted'}), 200

    except Exception as e:
        print(f"[ERROR] delete_history: {e}")
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    
    finally:
        if conn:
            conn.close()


# ======================================================
# SHARE HISTORY
# ======================================================
@history_bp.route('/<int:analysis_id>/share', methods=['POST'])
@jwt_required()
def share_history(analysis_id):
    user_id = get_jwt_identity()
    conn = None
    
    try:
        platform = request.json.get('platform', 'unknown') if request.json else 'unknown'
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'DB connection failed'}), 500

        cursor = conn.cursor()
        cursor.execute("""
            SELECT id
            FROM face_analyses
            WHERE id = %s AND user_id = %s
        """, (analysis_id, user_id))

        if not cursor.fetchone():
            cursor.close()
            return jsonify({'success': False, 'message': 'Data not found'}), 404

        cursor.close()

        # Log event
        try:
            log_event(user_id, 'SHARE', analysis_id, {'platform': platform})
        except Exception as e:
            print(f"[WARNING] Log failed: {e}")

        return jsonify({
            'success': True,
            'message': f'Shared to {platform}'
        }), 200

    except Exception as e:
        print(f"[ERROR] share_history: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    
    finally:
        if conn:
            conn.close()