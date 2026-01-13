from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_db_connection
import mysql.connector
from datetime import datetime

daily_logs_bp = Blueprint('daily_logs', __name__)

# ==================== FOODS API ====================

@daily_logs_bp.route('/api/foods', methods=['GET'])
@jwt_required()
def get_foods():
    """Ambil semua foods"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, oil, simple_carb, sugar, fiber, fermented FROM foods ORDER BY name ASC")
        foods = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'data': foods}), 200
    except Exception as e:
        print(f"Error in get_foods: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/foods/<int:food_id>', methods=['GET'])
@jwt_required()
def get_food(food_id):
    """Ambil detail food"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, oil, simple_carb, sugar, fiber, fermented FROM foods WHERE id = %s", (food_id,))
        food = cursor.fetchone()

        cursor.close()
        conn.close()

        if not food:
            return jsonify({'status': 'error', 'message': 'Food tidak ditemukan'}), 404

        return jsonify({'status': 'success', 'data': food}), 200
    except Exception as e:
        print(f"Error in get_food: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/foods', methods=['POST'])
@jwt_required()
def create_food():
    """Buat food baru"""
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        oil = data.get('oil', 0)
        simple_carb = data.get('simple_carb', 0)
        sugar = data.get('sugar', 0)
        fiber = data.get('fiber', 0)
        fermented = data.get('fermented', 0)

        if not name:
            return jsonify({'status': 'error', 'message': 'Nama food wajib diisi'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO foods (name, oil, simple_carb, sugar, fiber, fermented)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, oil, simple_carb, sugar, fiber, fermented))
        conn.commit()
        food_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Food berhasil dibuat',
            'data': {
                'id': food_id,
                'name': name,
                'oil': oil,
                'simple_carb': simple_carb,
                'sugar': sugar,
                'fiber': fiber,
                'fermented': fermented
            }
        }), 201
    except Exception as e:
        print(f"Error in create_food: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

# ==================== DAILY FOOD LOGS API ====================

@daily_logs_bp.route('/api/daily-food-logs', methods=['GET'])
@jwt_required()
def get_daily_food_logs():
    """Ambil daily food logs dengan filter"""
    try:
        user_id = get_jwt_identity() # Proteksi: ambil User ID dari token
        log_date = request.args.get('log_date')

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT fl.id, fl.user_id, fl.food_id, fl.quantity, fl.log_date,
                   f.name, f.oil, f.simple_carb, f.sugar, f.fiber, f.fermented
            FROM daily_food_logs fl
            JOIN foods f ON fl.food_id = f.id
            WHERE fl.user_id = %s
        """
        params = [user_id]

        if log_date:
            query += " AND fl.log_date = %s"
            params.append(log_date)

        query += " ORDER BY fl.log_date DESC, fl.id DESC"

        cursor.execute(query, params)
        logs = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'data': logs}), 200
    except Exception as e:
        print(f"Error in get_daily_food_logs: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/daily-food-logs', methods=['POST'])
@jwt_required()
def create_daily_food_log():
    """Buat daily food log baru"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        food_id = data.get('food_id')
        quantity = data.get('quantity', 1)
        log_date = data.get('log_date')

        if not food_id or not log_date:
            return jsonify({'status': 'error', 'message': 'food_id dan log_date wajib'}), 400

        if quantity <= 0:
            return jsonify({'status': 'error', 'message': 'Quantity harus > 0'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()

        # Check if food exists
        cursor.execute("SELECT id FROM foods WHERE id = %s", (food_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'status': 'error', 'message': 'Food tidak ditemukan'}), 404

        cursor.execute("""
            INSERT INTO daily_food_logs (user_id, food_id, quantity, log_date)
            VALUES (%s, %s, %s, %s)
        """, (user_id, food_id, quantity, log_date))
        conn.commit()
        log_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Food log berhasil dibuat',
            'data': {'id': log_id}
        }), 201
    except Exception as e:
        print(f"Error in create_daily_food_log: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/daily-food-logs/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_daily_food_log(log_id):
    """Hapus daily food log"""
    try:
        user_id = get_jwt_identity()
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        # Pastikan user hanya bisa menghapus log milik sendiri
        cursor.execute("DELETE FROM daily_food_logs WHERE id = %s AND user_id = %s", (log_id, user_id))
        conn.commit()

        deleted = cursor.rowcount > 0
        cursor.close()
        conn.close()

        if not deleted:
            return jsonify({'status': 'error', 'message': 'Log tidak ditemukan atau bukan milik Anda'}), 404

        return jsonify({'status': 'success', 'message': 'Log berhasil dihapus'}), 200
    except Exception as e:
        print(f"Error in delete_daily_food_log: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500
    
# ==================== DRINKS API ====================

@daily_logs_bp.route('/api/drinks', methods=['GET'])
@jwt_required()
def get_drinks():
    """Ambil semua drinks"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, drink_type, sugar
            FROM drinks
            ORDER BY name ASC
        """)
        drinks = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'data': drinks}), 200
    except Exception as e:
        print(f"Error in get_drinks: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/drinks/<int:drink_id>', methods=['GET'])
@jwt_required()
def get_drink(drink_id):
    """Ambil detail drink"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, drink_type, sugar
            FROM drinks
            WHERE id = %s
        """, (drink_id,))
        drink = cursor.fetchone()

        cursor.close()
        conn.close()

        if not drink:
            return jsonify({'status': 'error', 'message': 'Drink tidak ditemukan'}), 404

        return jsonify({'status': 'success', 'data': drink}), 200
    except Exception as e:
        print(f"Error in get_drink: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/drinks', methods=['POST'])
@jwt_required()
def create_drink():
    """Buat drink baru"""
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        drink_type = data.get('drink_type')
        sugar = data.get('sugar', 0)

        if not name or not drink_type:
            return jsonify({'status': 'error', 'message': 'Nama dan tipe drink wajib'}), 400

        if drink_type not in ('WATER', 'SWEET'):
            return jsonify({'status': 'error', 'message': 'drink_type tidak valid'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO drinks (name, drink_type, sugar)
            VALUES (%s, %s, %s)
        """, (name, drink_type, sugar))
        conn.commit()
        drink_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Drink berhasil dibuat',
            'data': {
                'id': drink_id,
                'name': name,
                'drink_type': drink_type,
                'sugar': sugar
            }
        }), 201
    except Exception as e:
        print(f"Error in create_drink: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/daily-drink-logs', methods=['GET'])
@jwt_required()
def get_daily_drink_logs():
    """Ambil daily drink logs dengan filter"""
    try:
        user_id = get_jwt_identity()
        log_date = request.args.get('log_date')

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT dl.id, dl.user_id, dl.drink_id, dl.quantity, dl.log_date,
                   d.name, d.drink_type, d.sugar
            FROM daily_drink_logs dl
            JOIN drinks d ON dl.drink_id = d.id
            WHERE dl.user_id = %s
        """
        params = [user_id]

        if log_date:
            query += " AND dl.log_date = %s"
            params.append(log_date)

        query += " ORDER BY dl.log_date DESC, dl.id DESC"

        cursor.execute(query, params)
        logs = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'data': logs}), 200
    except Exception as e:
        print(f"Error in get_daily_drink_logs: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/daily-drink-logs', methods=['POST'])
@jwt_required()
def create_daily_drink_log(): 
    """Buat daily drink log baru"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {} 
        drink_id = data.get('drink_id') 
        quantity = data.get('quantity', 1) 
        log_date = data.get('log_date')

        if not drink_id or not log_date:
            return jsonify({'status': 'error', 'message': 'drink_id dan log_date wajib'}), 400

        if quantity <= 0:
            return jsonify({'status': 'error', 'message': 'Quantity harus > 0'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()

        # Check if drink exists 
        cursor.execute("SELECT id FROM drinks WHERE id = %s", (drink_id,)) 
        if not cursor.fetchone(): 
            cursor.close() 
            conn.close() 
            return jsonify({'status': 'error', 'message': 'Drink tidak ditemukan'}), 404

        cursor.execute("""
            INSERT INTO daily_drink_logs (user_id, drink_id, quantity, log_date)
            VALUES (%s, %s, %s, %s)
        """, (user_id, drink_id, quantity, log_date))
        conn.commit()
        log_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Drink log berhasil dibuat',
            'data': {'id': log_id}
        }), 201
    except Exception as e:
        print(f"Error in create_daily_drink_log: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/daily-drink-logs/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_daily_drink_log(log_id):
    """Hapus daily drink log"""
    try:
        user_id = get_jwt_identity()
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("DELETE FROM daily_drink_logs WHERE id = %s AND user_id = %s", (log_id, user_id))
        conn.commit()

        deleted = cursor.rowcount > 0
        cursor.close()
        conn.close()

        if not deleted:
            return jsonify({'status': 'error', 'message': 'Log tidak ditemukan atau bukan milik Anda'}), 404

        return jsonify({'status': 'success', 'message': 'Log berhasil dihapus'}), 200
    except Exception as e:
        print(f"Error in delete_daily_drink_log: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

# ==================== DAILY SLEEP LOGS API ====================

@daily_logs_bp.route('/api/daily-sleep-logs', methods=['GET'])
@jwt_required()
def get_daily_sleep_logs():
    """Ambil daily sleep logs dengan filter"""
    try:
        user_id = get_jwt_identity()
        log_date = request.args.get('log_date')

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)

        query = "SELECT id, user_id, log_date, sleep_hours FROM daily_sleep_logs WHERE user_id = %s"
        params = [user_id]

        if log_date:
            query += " AND log_date = %s"
            params.append(log_date)

        query += " ORDER BY log_date DESC"

        cursor.execute(query, params)
        logs = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'data': logs}), 200
    except Exception as e:
        print(f"Error in get_daily_sleep_logs: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/daily-sleep-logs', methods=['POST'])
@jwt_required()
def create_daily_sleep_log():
    """Buat daily sleep log baru"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        log_date = data.get('log_date')
        sleep_hours = data.get('sleep_hours', 0.0)

        if not log_date:
            return jsonify({'status': 'error', 'message': 'log_date wajib'}), 400

        if sleep_hours < 0 or sleep_hours > 24:
            return jsonify({'status': 'error', 'message': 'Sleep hours harus 0-24'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO daily_sleep_logs (user_id, log_date, sleep_hours)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE sleep_hours = VALUES(sleep_hours)
        """, (user_id, log_date, sleep_hours))
        conn.commit()
        log_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Sleep log berhasil dibuat/diupdate',
            'data': {'id': log_id}
        }), 201
    except Exception as e:
        print(f"Error in create_daily_sleep_log: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

# ==================== SKIN ANALYSIS API ====================

def calculate_daily_aggregates(user_id, log_date):
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT
            COALESCE(SUM(f.oil * fl.quantity), 0) AS total_oil,
            COALESCE(SUM(f.simple_carb * fl.quantity), 0) AS total_simple_carb,
            COALESCE(SUM(f.sugar * fl.quantity), 0) AS food_sugar,
            COALESCE(SUM(f.fiber * fl.quantity), 0) AS total_fiber,
            COALESCE(SUM(f.fermented * fl.quantity), 0) AS total_fermented,

            COALESCE(SUM(
                CASE WHEN d.drink_type = 'WATER'
                THEN dl.quantity ELSE 0 END
            ), 0) AS hydration,

            COALESCE(SUM(
                CASE WHEN d.drink_type = 'SWEET'
                THEN d.sugar * dl.quantity ELSE 0 END
            ), 0) AS liquid_sugar,

            COALESCE(sl.sleep_hours, 0) AS sleep_hours
        FROM users u
        LEFT JOIN daily_food_logs fl
            ON u.id = fl.user_id AND fl.log_date = %s
        LEFT JOIN foods f ON fl.food_id = f.id
        LEFT JOIN daily_drink_logs dl
            ON u.id = dl.user_id AND dl.log_date = %s
        LEFT JOIN drinks d ON dl.drink_id = d.id
        LEFT JOIN daily_sleep_logs sl
            ON u.id = sl.user_id AND sl.log_date = %s
        WHERE u.id = %s
        GROUP BY u.id, sl.sleep_hours
    """, (log_date, log_date, log_date, user_id))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return rows[0] if rows else None


def calculate_skin_load_score(aggregates):
    """Hitung skin load score berdasarkan formula"""
    total_oil = float(aggregates['total_oil'])
    total_simple_carb = float(aggregates['total_simple_carb'])
    total_sugar = float(aggregates['food_sugar']) + float(aggregates['liquid_sugar'])
    total_fiber = float(aggregates['total_fiber'])
    total_fermented = float(aggregates['total_fermented'])
    hydration = float(aggregates['hydration'])
    sleep_hours = float(aggregates['sleep_hours'])

    # Base score: (oil + carb + sugar) - (fiber + fermented)
    base_score = (total_oil + total_simple_carb + total_sugar) - (total_fiber + total_fermented)

    # Hydration bonus (max 2 points if drink 8 glasses)
    hydration_bonus = min(hydration / 8.0, 1.0) * 2.0

    # Sleep deficit penalty (target 8 hours)
    sleep_deficit = max(0, 8.0 - sleep_hours)

    skin_load_score = base_score - hydration_bonus + sleep_deficit

    return skin_load_score

def determine_skin_status(skin_load_score):
    """Tentukan status berdasarkan score"""
    if skin_load_score <= 5:
        return 'AMAN'
    elif skin_load_score <= 10:
        return 'WASPADA'
    else:
        return 'OVER_LIMIT'

def get_main_triggers(aggregates, skin_load_score):
    """Tentukan trigger utama berdasarkan aggregates"""
    triggers = []

    if float(aggregates['total_oil']) > 10:
        triggers.append("Konsumsi minyak/gorengan berlebih")
    if float(aggregates['total_simple_carb']) > 15:
        triggers.append("Konsumsi karbohidrat sederhana tinggi")
    if (float(aggregates['food_sugar']) + float(aggregates['liquid_sugar'])) > 10:
        triggers.append("Konsumsi gula berlebih")
    if float(aggregates['total_fiber']) < 5:
        triggers.append("Serat kurang")
    if float(aggregates['hydration']) < 6:
        triggers.append("Hidrasi kurang")
    if float(aggregates['sleep_hours']) < 7:
        triggers.append("Tidur kurang")

    return "; ".join(triggers) if triggers else "Tidak ada trigger signifikan"

@daily_logs_bp.route('/api/skin-analysis', methods=['GET'])
@jwt_required()
def get_skin_analysis():
    """Ambil skin analysis dengan filter"""
    try:
        user_id = get_jwt_identity()
        log_date = request.args.get('log_date')

        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT id, user_id, log_date, total_oil, total_simple_carb, total_sugar,
                   total_fiber, total_fermented, hydration, sleep_deficit,
                   skin_load_score, status, main_triggers, created_at
            FROM daily_skin_analysis WHERE user_id = %s
        """
        params = [user_id]

        if log_date:
            query += " AND log_date = %s"
            params.append(log_date)

        query += " ORDER BY log_date DESC"

        cursor.execute(query, params)
        analyses = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'data': analyses}), 200
    except Exception as e:
        print(f"Error in get_skin_analysis: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/skin-analysis', methods=['POST'])
@jwt_required()
def generate_skin_analysis():
    """Generate analisis kulit harian"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        log_date = data.get('log_date')

        if not log_date:
            return jsonify({'status': 'error', 'message': 'log_date wajib'}), 400

        # Hitung aggregates
        aggregates = calculate_daily_aggregates(user_id, log_date)

        if not aggregates:
            return jsonify({'status': 'error', 'message': 'Tidak ada data untuk tanggal tersebut'}), 404

        # Hitung skin load score
        skin_load_score = calculate_skin_load_score(aggregates)
        status = determine_skin_status(skin_load_score)
        main_triggers = get_main_triggers(aggregates, skin_load_score)

        # Simpan ke database
        conn = get_db_connection()
        if not conn:
            return jsonify({'status': 'error', 'message': 'Gagal terhubung ke database'}), 500

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO daily_skin_analysis
            (user_id, log_date, total_oil, total_simple_carb, total_sugar, total_fiber,
             total_fermented, hydration, sleep_deficit, skin_load_score, status, main_triggers)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            total_oil=VALUES(total_oil), total_simple_carb=VALUES(total_simple_carb),
            total_sugar=VALUES(total_sugar), total_fiber=VALUES(total_fiber),
            total_fermented=VALUES(total_fermented), hydration=VALUES(hydration),
            sleep_deficit=VALUES(sleep_deficit), skin_load_score=VALUES(skin_load_score),
            status=VALUES(status), main_triggers=VALUES(main_triggers)
        """, (
            user_id, log_date,
            aggregates['total_oil'], aggregates['total_simple_carb'],
            aggregates['food_sugar'] + aggregates['liquid_sugar'],  # total_sugar
            aggregates['total_fiber'], aggregates['total_fermented'],
            aggregates['hydration'], max(0, 8.0 - aggregates['sleep_hours']),  # sleep_deficit
            skin_load_score, status, main_triggers
        ))

        conn.commit()
        analysis_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Analisis kulit berhasil di-generate',
            'data': {
                'id': analysis_id,
                'skin_load_score': skin_load_score,
                'status': status,
                'main_triggers': main_triggers,
                'aggregates': aggregates
            }
        }), 201
    except Exception as e:
        print(f"Error in generate_skin_analysis: {e}")
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan server'}), 500

@daily_logs_bp.route('/api/skin-analysis/history', methods=['GET'])
@jwt_required()
def get_analysis_history():
    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500

        cursor = conn.cursor(dictionary=True, buffered=True)

        query = """
            SELECT 
                dsa.log_date,
                dsa.skin_load_score,
                dsa.status,
                dsa.main_triggers,
                COALESCE(dsl.sleep_hours, 0) AS sleep_hours,

                (
                    SELECT GROUP_CONCAT(f.name SEPARATOR ', ')
                    FROM daily_food_logs dfl
                    JOIN foods f ON dfl.food_id = f.id
                    WHERE dfl.user_id = dsa.user_id
                      AND dfl.log_date = dsa.log_date
                ) AS foods,

                (
                    SELECT GROUP_CONCAT(d.name SEPARATOR ', ')
                    FROM daily_drink_logs ddl
                    JOIN drinks d ON ddl.drink_id = d.id
                    WHERE ddl.user_id = dsa.user_id
                      AND ddl.log_date = dsa.log_date
                ) AS drinks

            FROM daily_skin_analysis dsa
            LEFT JOIN daily_sleep_logs dsl
                ON dsa.user_id = dsl.user_id
               AND dsa.log_date = dsl.log_date
            WHERE dsa.user_id = %s
            ORDER BY dsa.log_date DESC
            LIMIT 7
        """

        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        history = []
        for row in rows:
            history.append({
                "date": row["log_date"].isoformat(),
                "skin_load_score": float(row["skin_load_score"]),
                "status": row["status"],
                "main_triggers": row["main_triggers"],
                "sleep_hours": float(row["sleep_hours"]),
                "foods": row["foods"] or "-",
                "drinks": row["drinks"] or "-"
            })

        return jsonify({'success': True, 'data': history}), 200

    except Exception as e:
        print(f"Error in get_analysis_history: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500
