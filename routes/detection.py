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
from datetime import datetime
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

LABELS_TYPE = ['Berminyak', 'Kering', 'Normal'] 
LABELS_PROBLEM = ['Berjerawat', 'Dermatitis Perioral atau Ruam', 'Normal']

# File size limit (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Global model cache
_model_type = None
_model_problem = None
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
            analysis_data['timestamp'],
            analysis_data['image_filename'],
            analysis_data['image_url'],
            analysis_data['skin_type_analysis']['result'],
            float(analysis_data['skin_type_analysis']['confidence'].rstrip('%')),
            json.dumps(analysis_data['skin_type_analysis']['all_predictions']),
            analysis_data['skin_problem_analysis']['result'],
            float(analysis_data['skin_problem_analysis']['confidence'].rstrip('%')),
            json.dumps(analysis_data['skin_problem_analysis']['all_predictions'])
        )
        
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Analysis {analysis_data['analysis_id']} saved to database for user {user_id}")
        return True
    except Exception as e:
        print(f"❌ Error saving analysis to database: {e}")
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
            'problem': _model_problem is not None
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
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
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
        image_url = f'/static/uploads/analyses/{saved_filename}'
        
        # Prepare response data
        analysis_data = {
            'success': True,
            'analysis_id': analysis_id,
            'timestamp': timestamp,
            'image_url': image_url,
            'image_filename': saved_filename,
            'skin_type_analysis': type_result,
            'skin_problem_analysis': problem_result
        }
        
        # Save to database in background thread (non-blocking)
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
                    'image_url': row['image_url'].replace('/uploads/', '/static/uploads/'),
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