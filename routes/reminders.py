from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from routes.auth import get_db_connection

reminder_bp = Blueprint('reminder', __name__)

# ===============================
# GET REMINDER USER
# ===============================
@reminder_bp.route('/api/reminders', methods=['GET'])
@jwt_required()
def get_reminders():
    try:
        user_id = int(get_jwt_identity())
        print("GET REMINDER USER:", user_id)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT type, hour, minute, is_active
            FROM glowmate
            WHERE user_id = %s
        """, (user_id,))

        data = cursor.fetchall()
        conn.close()

        return jsonify(data), 200

    except Exception as e:
        print("REMINDER GET ERROR:", e)
        return jsonify({'error': str(e)}), 500



# ===============================
# SAVE / UPDATE REMINDER
# ===============================
@reminder_bp.route('/api/reminders', methods=['POST'])
@jwt_required()
def save_reminder():
    try:
        user_id = int(get_jwt_identity())
        data = request.json

        is_active = 1 if data['is_active'] else 0

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM glowmate
            WHERE user_id=%s AND type=%s
        """, (user_id, data['type']))

        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE glowmate
                SET hour=%s, minute=%s, is_active=%s, updated_at=NOW()
                WHERE user_id=%s AND type=%s
            """, (
                data['hour'],
                data['minute'],
                is_active,
                user_id,
                data['type']
            ))
        else:
            cursor.execute("""
                INSERT INTO glowmate
                (user_id, type, hour, minute, is_active)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                user_id,
                data['type'],
                data['hour'],
                data['minute'],
                is_active
            ))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Reminder saved'}), 200

    except Exception as e:
        print("REMINDER SAVE ERROR:", e)
        return jsonify({'error': str(e)}), 500
