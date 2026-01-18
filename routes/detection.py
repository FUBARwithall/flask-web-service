from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import numpy as np
import keras
from PIL import Image
import cv2
import json
import threading
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from datetime import datetime, timezone, timedelta
import uuid
from models import get_db_connection

print(f"INFO: Using Keras version {keras.__version__}")

detection_bp = Blueprint('detection', __name__, url_prefix='/api/detection')

# ============================================
# OPTIMIZED CONFIGURATION
# ============================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_TYPE_PATH = os.path.join(BASE_DIR, 'ml_models', 'model_jeniskulit.keras')
MODEL_PROBLEM_PATH = os.path.join(BASE_DIR, 'ml_models', 'model_masalah_kulit.keras')
MODEL_BODY_PATH = os.path.join(BASE_DIR, 'ml_models', 'model_penyakit_tubuh.keras')
METADATA_BODY_PATH = os.path.join(BASE_DIR, 'ml_models', 'metadata_penyakit.json')

LABELS_TYPE = ['Berminyak', 'Kering', 'Normal'] 
LABELS_PROBLEM = ['Berjerawat', 'Dermatitis Perioral atau Ruam', 'Normal']
# Labels for body skin disease (alphabetically sorted as per Keras convention)
LABELS_BODY = ['eksim', 'impetigo', 'kudis', 'kurap', 'psoriasis', 'varicella', 'vitiligo']

# File size limit (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Global model cache
_model_type = None
_model_problem = None
_model_body = None
_metadata_body = None
_clahe = None

def get_clahe():
    """Cache CLAHE object"""
    global _clahe
    if _clahe is None:
        _clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return _clahe

def load_type_model():
    """Lazy load skin type model"""
    global _model_type
    if _model_type is None:
        if not os.path.exists(MODEL_TYPE_PATH):
            raise FileNotFoundError(f"Type model not found: {MODEL_TYPE_PATH}")
        
        print("📥 Loading Skin Type model...")
        _model_type = keras.saving.load_model(MODEL_TYPE_PATH, compile=False)
        print("✅ Skin Type model loaded")
    return _model_type

def load_problem_model():
    """Lazy load skin problem model"""
    global _model_problem
    if _model_problem is None:
        if not os.path.exists(MODEL_PROBLEM_PATH):
            raise FileNotFoundError(f"Problem model not found: {MODEL_PROBLEM_PATH}")
        
        print("📥 Loading Skin Problem model...")
        _model_problem = keras.saving.load_model(MODEL_PROBLEM_PATH, compile=False)
        print("✅ Skin Problem model loaded")
    return _model_problem

def load_body_model():
    """Lazy load body skin disease model"""
    global _model_body
    if _model_body is None:
        if not os.path.exists(MODEL_BODY_PATH):
            raise FileNotFoundError(f"Body model not found: {MODEL_BODY_PATH}")
        
        print("📥 Loading Body Skin Disease model...")
        _model_body = keras.saving.load_model(MODEL_BODY_PATH, compile=False)
        print("✅ Body Skin Disease model loaded")
    return _model_body

def load_body_metadata():
    """Lazy load body disease metadata"""
    global _metadata_body
    if _metadata_body is None:
        if not os.path.exists(METADATA_BODY_PATH):
            raise FileNotFoundError(f"Metadata not found: {METADATA_BODY_PATH}")
        
        with open(METADATA_BODY_PATH, 'r', encoding='utf-8') as f:
            _metadata_body = json.load(f)
        print("✅ Body disease metadata loaded")
    return _metadata_body

def allowed_file(filename):
    """Validate file extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(filepath):
    """Optimized image preprocessing - returns reusable array"""
    # Load image using PIL (faster than Keras for this use case)
    img = Image.open(filepath).convert('RGB')
    img_np = np.array(img, dtype=np.uint8)
    
    # Apply CLAHE for better feature detection
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    enhanced = get_clahe().apply(gray)
    img_rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
    
    # Resize and normalize
    img_resized = cv2.resize(img_rgb, (224, 224), interpolation=cv2.INTER_AREA)
    img_array = np.expand_dims(img_resized, axis=0).astype(np.float32) / 255.0
    
    return img_array

def predict_with_array(model, labels, img_array):
    """Optimized prediction using pre-processed array (no redundant preprocessing)"""
    # Predict (verbose=0 to suppress output)
    predictions = model.predict(img_array, verbose=0)[0]
    
    # Get results
    class_idx = int(np.argmax(predictions))
    confidence = float(predictions[class_idx])
    
    return {
        'result': labels[class_idx],
        'confidence': f"{confidence * 100:.2f}%",
        'all_predictions': {
            labels[i]: round(float(predictions[i]) * 100, 2) 
            for i in range(len(labels))
        }
    }

def save_face_analysis_to_db(user_id, analysis_data):
    """Save face analysis results to database (runs in background thread)"""
    print(f"📝 save_face_analysis_to_db called for user {user_id}")
    print(f"📝 Analysis ID: {analysis_data.get('analysis_id')}")
    print(f"📝 Timestamp DB: {analysis_data.get('timestamp_db')}")
    print(f"📝 Timestamp DB type: {type(analysis_data.get('timestamp_db'))}")
    
    conn = get_db_connection()
    if not conn:
        print("ERROR: Could not connect to database for saving analysis")
        return False
    
    try:
        cursor = conn.cursor()
        
        query = """
            INSERT INTO face_analyses 
            (id, user_id, timestamp, image_filename, image_url,
             skin_type, skin_type_confidence, skin_type_predictions,
             skin_problem, skin_problem_confidence, skin_problem_predictions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            analysis_data['analysis_id'],
            user_id,
            analysis_data['timestamp_db'],  # Use datetime object for MySQL
            analysis_data['image_filename'],
            analysis_data['image_url'],
            analysis_data['skin_type_analysis']['result'],
            float(analysis_data['skin_type_analysis']['confidence'].rstrip('%')),
            json.dumps(analysis_data['skin_type_analysis']['all_predictions']),
            analysis_data['skin_problem_analysis']['result'],
            float(analysis_data['skin_problem_analysis']['confidence'].rstrip('%')),
            json.dumps(analysis_data['skin_problem_analysis']['all_predictions'])
        )
        
        print(f"📝 Executing query with values: {values[0]}, {values[1]}, {values[2]}")
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Analysis {analysis_data['analysis_id']} saved to database for user {user_id}")
        return True
    except Exception as e:
        print(f"❌ Error saving analysis to database: {e}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        if conn:
            conn.close()
        return False

@detection_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'models_loaded': {
            'type': _model_type is not None,
            'problem': _model_problem is not None,
            'body': _model_body is not None
        }
    })

@detection_bp.route('/debug-upload', methods=['GET'])
@jwt_required()
def debug_upload():
    """Debug endpoint - requires authentication"""
    analyses_folder = os.path.join(UPLOAD_FOLDER, 'analyses')
    return jsonify({
        'UPLOAD_FOLDER': UPLOAD_FOLDER,
        'analyses_folder': analyses_folder,
        'analyses_exists': os.path.exists(analyses_folder),
        'files': os.listdir(analyses_folder) if os.path.exists(analyses_folder) else [],
        'permissions': oct(os.stat(UPLOAD_FOLDER).st_mode)[-3:] if os.path.exists(UPLOAD_FOLDER) else 'N/A'
    })

@detection_bp.route('/detect', methods=['POST'])
@jwt_required()
def detect_all():
    """Optimized detection endpoint with image saving and database storage"""
    # Get user_id from JWT token
    user_id = get_jwt_identity()
    
    # Validate request
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'File type not allowed'}), 400

    # Validate file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'success': False, 'message': 'File too large (max 10MB)'}), 400

    # Generate unique identifiers
    analysis_id = str(uuid.uuid4())
    # WIB = UTC+7
    wib = timezone(timedelta(hours=7))
    timestamp_dt = datetime.now(wib)  # datetime object for database
    timestamp_str = timestamp_dt.isoformat()  # ISO string for API response
    
    # Create analyses folder if it doesn't exist
    analyses_folder = os.path.join(UPLOAD_FOLDER, 'analyses')
    os.makedirs(analyses_folder, exist_ok=True)
    
    # Save with unique filename (preserves extension)
    file_ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
    saved_filename = f"{analysis_id}.{file_ext}"
    saved_filepath = os.path.join(analyses_folder, saved_filename)
    
    try:
        file.save(saved_filepath)
        
        # Load models (lazy, only once per model)
        m_type = load_type_model()
        m_problem = load_problem_model()
        
        # Preprocess ONCE, use for both predictions
        img_array = preprocess_image(saved_filepath)
        
        # Run predictions using the same preprocessed array
        type_result = predict_with_array(m_type, LABELS_TYPE, img_array)
        problem_result = predict_with_array(m_problem, LABELS_PROBLEM, img_array)
        
        # Image URL for frontend (relative path)
        image_url = f'/uploads/analyses/{saved_filename}'
        
        # Prepare response data
        analysis_data = {
            'success': True,
            'analysis_id': analysis_id,
            'timestamp': timestamp_str,  # ISO string for frontend
            'timestamp_db': timestamp_dt,  # datetime object for database
            'image_url': image_url,
            'image_filename': saved_filename,
            'skin_type_analysis': type_result,
            'skin_problem_analysis': problem_result
        }
        
        # Save to database in background thread (non-blocking)
        print(f"🔄 Starting background thread to save analysis {analysis_id} for user {user_id}")
        print(f"📅 Timestamp for DB: {timestamp_dt}")
        print(f"📅 Timestamp for API: {timestamp_str}")
        threading.Thread(
            target=save_face_analysis_to_db, 
            args=(user_id, analysis_data),
            daemon=True
        ).start()
        
        return jsonify(analysis_data)

    except FileNotFoundError as e:
        # Clean up file if it exists
        if os.path.exists(saved_filepath):
            os.remove(saved_filepath)
        return jsonify({
            'success': False, 
            'message': f'Model file not found: {str(e)}'
        }), 500
        
    except Exception as e:
        # Clean up file if it exists
        if os.path.exists(saved_filepath):
            os.remove(saved_filepath)
        return jsonify({
            'success': False, 
            'message': f'Error during prediction: {str(e)}'
        }), 500

@detection_bp.route('/history', methods=['GET'])
@jwt_required()
def get_user_history():
    """Get detection history for the authenticated user"""
    user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, timestamp, image_url, skin_type, skin_problem
            FROM face_analyses
            WHERE user_id = %s
            ORDER BY timestamp DESC
            LIMIT 50
        """, (user_id,))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'history': [
                {
                    'analysis_id': row['id'],
                    'timestamp': row['timestamp'],
                    'image_url': row['image_url'],
                    'skin_type': row['skin_type'],
                    'skin_problem': row['skin_problem']
                }
                for row in results
            ]
        })
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({
            'success': False,
            'message': f'Error retrieving history: {str(e)}'
        }), 500


# ============================================
# BODY SKIN DISEASE DETECTION
# ============================================

def save_body_analysis_to_db(user_id, analysis_data):
    """Save body skin analysis results to database (runs in background thread)"""
    conn = get_db_connection()
    if not conn:
        print("ERROR: Could not connect to database for saving body analysis")
        return False
    
    try:
        cursor = conn.cursor()
        
        query = """
            INSERT INTO body_analyses 
            (id, user_id, timestamp, image_filename, image_url,
             disease_key, disease_name, confidence, all_predictions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            analysis_data['analysis_id'],
            user_id,
            analysis_data['timestamp_db'],  # Use datetime object for MySQL
            analysis_data['image_filename'],
            analysis_data['image_url'],
            analysis_data['disease_analysis']['disease_key'],
            analysis_data['disease_analysis']['disease_info']['nama'],
            float(analysis_data['disease_analysis']['confidence'].rstrip('%')),
            json.dumps(analysis_data['disease_analysis']['all_predictions'])
        )
        
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Body analysis {analysis_data['analysis_id']} saved to database for user {user_id}")
        return True
    except Exception as e:
        print(f"❌ Error saving body analysis to database: {e}")
        if conn:
            conn.close()
        return False


@detection_bp.route('/detect-body', methods=['POST'])
@jwt_required()
def detect_body_disease():
    """Detect skin disease on body parts using ML model"""
    # Get user_id from JWT token
    user_id = get_jwt_identity()
    
    # Validate request
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'File type not allowed'}), 400

    # Validate file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'success': False, 'message': 'File too large (max 10MB)'}), 400

    # Generate unique identifiers
    analysis_id = str(uuid.uuid4())
    # WIB = UTC+7
    wib = timezone(timedelta(hours=7))
    timestamp_dt = datetime.now(wib)  # datetime object for database
    timestamp_str = timestamp_dt.isoformat()  # ISO string for API response
    
    # Create body_analyses folder if it doesn't exist
    body_folder = os.path.join(UPLOAD_FOLDER, 'body_analyses')
    os.makedirs(body_folder, exist_ok=True)
    
    # Save with unique filename (preserves extension)
    file_ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
    saved_filename = f"{analysis_id}.{file_ext}"
    saved_filepath = os.path.join(body_folder, saved_filename)
    
    try:
        file.save(saved_filepath)
        
        # Load model and metadata
        m_body = load_body_model()
        metadata = load_body_metadata()
        
        # Preprocess image
        img_array = preprocess_image(saved_filepath)
        
        # Run prediction
        predictions = m_body.predict(img_array, verbose=0)[0]
        class_idx = int(np.argmax(predictions))
        confidence = float(predictions[class_idx])
        disease_key = LABELS_BODY[class_idx]
        
        # Get disease info from metadata
        disease_info = metadata.get(disease_key, {
            'nama': disease_key.capitalize(),
            'deskripsi': 'Informasi tidak tersedia',
            'gejala': [],
            'obat': []
        })
        
        # Build all predictions dict
        all_predictions = {
            LABELS_BODY[i]: round(float(predictions[i]) * 100, 2) 
            for i in range(len(LABELS_BODY))
        }
        
        # Image URL for frontend (relative path)
        image_url = f'/uploads/body_analyses/{saved_filename}'
        
        # Prepare response data
        analysis_data = {
            'success': True,
            'analysis_id': analysis_id,
            'timestamp': timestamp_str,  # ISO string for frontend
            'timestamp_db': timestamp_dt,  # datetime object for database
            'image_url': image_url,
            'image_filename': saved_filename,
            'disease_analysis': {
                'disease_key': disease_key,
                'confidence': f"{confidence * 100:.2f}%",
                'all_predictions': all_predictions,
                'disease_info': {
                    'nama': disease_info.get('nama', disease_key.capitalize()),
                    'deskripsi': disease_info.get('deskripsi', ''),
                    'gejala': disease_info.get('gejala', []),
                    'obat': disease_info.get('obat', [])
                }
            }
        }
        
        # Save to database in background thread (non-blocking)
        threading.Thread(
            target=save_body_analysis_to_db, 
            args=(user_id, analysis_data),
            daemon=True
        ).start()
        
        return jsonify(analysis_data)

    except FileNotFoundError as e:
        # Clean up file if it exists
        if os.path.exists(saved_filepath):
            os.remove(saved_filepath)
        return jsonify({
            'success': False, 
            'message': f'Model file not found: {str(e)}'
        }), 500
        
    except Exception as e:
        # Clean up file if it exists
        if os.path.exists(saved_filepath):
            os.remove(saved_filepath)
        return jsonify({
            'success': False, 
            'message': f'Error during prediction: {str(e)}'
        }), 500



@detection_bp.route('/body-history', methods=['GET'])
@jwt_required()
def get_body_history():
    """Get body disease detection history for the authenticated user"""
    user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, timestamp, image_url, disease_key, disease_name, confidence
            FROM body_analyses
            WHERE user_id = %s
            ORDER BY timestamp DESC
            LIMIT 50
        """, (user_id,))
        
        results = cursor.fetchall()
        
        # Convert timestamps to WIB (UTC+7)
        wib = timezone(timedelta(hours=7))
        for item in results:
            if item.get('timestamp') and isinstance(item['timestamp'], datetime):
                # Jika timestamp dari DB tidak punya timezone, assume UTC dan convert ke WIB
                if item['timestamp'].tzinfo is None:
                    item['timestamp'] = item['timestamp'].replace(tzinfo=timezone.utc).astimezone(wib).isoformat()
                else:
                    item['timestamp'] = item['timestamp'].astimezone(wib).isoformat()
            elif item.get('timestamp'):
                item['timestamp'] = str(item['timestamp'])
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'history': [
                {
                    'analysis_id': row['id'],
                    'timestamp': row['timestamp'],
                    'image_url': row['image_url'],
                    'disease_key': row['disease_key'],
                    'disease_name': row['disease_name'],
                    'confidence': row['confidence']
                }
                for row in results
            ]
        })
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({
            'success': False,
            'message': f'Error retrieving body history: {str(e)}'
        }), 500


@detection_bp.route('/body-history/<string:analysis_id>', methods=['GET'])
@jwt_required()
def get_body_history_detail(analysis_id):
    """Get body disease detection detail for a specific analysis"""
    user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                id,
                timestamp,
                image_filename,
                image_url,
                disease_key,
                disease_name,
                confidence,
                all_predictions,
                note
            FROM body_analyses
            WHERE id = %s AND user_id = %s
        """, (analysis_id, user_id))
        
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            conn.close()
            return jsonify({'success': False, 'message': 'Data not found'}), 404
        
        # Load metadata to get disease info
        metadata = load_body_metadata()
        disease_key = row['disease_key']
        disease_info = metadata.get(disease_key, {
            'nama': disease_key.capitalize(),
            'deskripsi': 'Informasi tidak tersedia',
            'gejala': [],
            'obat': []
        })
        
        # Convert timestamp to WIB (UTC+7)
        wib = timezone(timedelta(hours=7))
        timestamp_value = row['timestamp']
        
        if timestamp_value and isinstance(timestamp_value, datetime):
            # Jika timestamp dari DB tidak punya timezone, assume UTC dan convert ke WIB
            if timestamp_value.tzinfo is None:
                timestamp_str = timestamp_value.replace(tzinfo=timezone.utc).astimezone(wib).isoformat()
            else:
                timestamp_str = timestamp_value.astimezone(wib).isoformat()
        elif timestamp_value:
            timestamp_str = str(timestamp_value)
        else:
            timestamp_str = None
        
        # Format response
        data = {
            'timestamp': timestamp_str,
            'image_url': row['image_url'] if row.get('image_url') else None,
            'disease_analysis': {
                'disease_key': disease_key,
                'disease_name': row['disease_name'],
                'confidence': row['confidence'],
                'all_predictions': row.get('all_predictions') or {},
                'disease_info': {
                    'nama': disease_info.get('nama', disease_key.capitalize()),
                    'deskripsi': disease_info.get('deskripsi', ''),
                    'gejala': disease_info.get('gejala', []),
                    'obat': disease_info.get('obat', [])
                }
            },
            'note': row.get('note')
        }
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except Exception as e:
        if conn:
            conn.close()
        print(f"[ERROR] get_body_history_detail: {e}")
        return jsonify({
            'success': False,
            'message': f'Error retrieving body history detail: {str(e)}'
        }), 500


@detection_bp.route('/body-history/<string:analysis_id>/notes', methods=['PATCH'])
@jwt_required()
def update_body_notes(analysis_id):
    """Update or delete notes for a body analysis"""
    user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    
    try:
        # Get notes from request body
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Request body required'}), 400
        
        notes = data.get('notes', '')  # Empty string = delete notes
        
        cursor = conn.cursor()
        
        # Check if analysis exists and belongs to user
        cursor.execute("""
            SELECT id FROM body_analyses
            WHERE id = %s AND user_id = %s
        """, (analysis_id, user_id))
        
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Data not found'}), 404
        
        # Update note
        cursor.execute("""
            UPDATE body_analyses
            SET note = %s
            WHERE id = %s AND user_id = %s
        """, (notes if notes else None, analysis_id, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Note updated successfully',
            'note': notes if notes else None
        }), 200
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        print(f"[ERROR] update_body_notes: {e}")
        return jsonify({
            'success': False,
            'message': f'Error updating notes: {str(e)}'
        }), 500


@detection_bp.route('/body-history/<string:analysis_id>', methods=['DELETE'])
@jwt_required()
def delete_body_history(analysis_id):
    """Delete body disease detection history"""
    user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get image filename first
        cursor.execute("""
            SELECT image_filename
            FROM body_analyses
            WHERE id = %s AND user_id = %s
        """, (analysis_id, user_id))
        row = cursor.fetchone()
        
        if not row:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Data not found'}), 404
        
        # Delete from database
        cursor.execute("""
            DELETE FROM body_analyses
            WHERE id = %s AND user_id = %s
        """, (analysis_id, user_id))
        
        conn.commit()
        cursor.close()
        
        # Delete image file (optional, with error handling)
        if row.get('image_filename'):
            try:
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                image_path = os.path.join(BASE_DIR, 'static/uploads/body_analyses', row['image_filename'])
                if os.path.exists(image_path):
                    os.remove(image_path)
                    print(f"[INFO] Deleted body image: {image_path}")
            except Exception as e:
                print(f"[WARNING] Failed to delete body image: {e}")
        
        conn.close()
        
        return jsonify({'success': True, 'message': 'Body history deleted'}), 200
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        print(f"[ERROR] delete_body_history: {e}")
        return jsonify({
            'success': False,
            'message': f'Error deleting body history: {str(e)}'
        }), 500
