from flask import Blueprint, request, jsonify
import os
import numpy as np
# Use Keras 3 directly (models were saved with Keras 3)
import keras
from keras.utils import load_img, img_to_array
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename

print(f"INFO: Using Keras version {keras.__version__}")
detection_bp = Blueprint('detection', __name__, url_prefix='/api/detection')
# ============================================
# MODEL CONFIGURATION
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_TYPE_PATH = os.path.join(BASE_DIR, 'ml_models', 'model_jeniskulit.keras')
MODEL_PROBLEM_PATH = os.path.join(BASE_DIR, 'ml_models', 'model_masalah_kulit.keras')
LABELS_TYPE = ['Berminyak', 'Kering', 'Normal'] 
LABELS_PROBLEM = ['Jerawat', 'Kusam', 'Penuaan'] 
model_type = None
model_problem = None
last_error_type = "Not attempted"
last_error_problem = "Not attempted"
def load_type_model():
    global model_type, last_error_type
    if model_type is None:
        print(f"INFO: Loading Skin Type model...")
        if os.path.exists(MODEL_TYPE_PATH):
            try:
                # Use Keras 3 native load_model
                model_type = keras.saving.load_model(MODEL_TYPE_PATH, compile=False)
                print("SUCCESS: Skin Type model loaded")
                last_error_type = "None"
            except Exception as e:
                last_error_type = str(e)
                print(f"ERROR: {last_error_type}")
        else:
            last_error_type = "File not found"
    return model_type
def load_problem_model():
    global model_problem, last_error_problem
    if model_problem is None:
        print(f"INFO: Loading Skin Problem model...")
        if os.path.exists(MODEL_PROBLEM_PATH):
            try:
                # Use Keras 3 native load_model
                model_problem = keras.saving.load_model(MODEL_PROBLEM_PATH, compile=False)
                print("SUCCESS: Skin Problem model loaded")
                last_error_problem = "None"
            except Exception as e:
                last_error_problem = str(e)
                print(f"ERROR: {last_error_problem}")
        else:
            last_error_problem = "File not found"
    return model_problem

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_image(m, labels, filepath):
    img = load_img(filepath, target_size=(224, 224)) 
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    predictions = m.predict(img_array)
    class_idx = np.argmax(predictions[0])
    confidence = float(predictions[0][class_idx])
    
    return {
        'result': labels[class_idx],
        'confidence': f"{confidence * 100:.2f}%",
        'all_predictions': {labels[i]: round(float(predictions[0][i]), 4) for i in range(len(labels))}
    }

@detection_bp.route('/detect', methods=['POST'])
def detect_all():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            m_type = load_type_model()
            m_problem = load_problem_model()

            if not m_type and not m_problem:
                 return jsonify({
                    'success': False, 
                    'message': 'Failed to load both models.',
                    'debug': {
                        'type_path': MODEL_TYPE_PATH,
                        'problem_path': MODEL_PROBLEM_PATH,
                        'type_exists': os.path.exists(MODEL_TYPE_PATH),
                        'problem_exists': os.path.exists(MODEL_PROBLEM_PATH),
                        'type_error': last_error_type,
                        'problem_error': last_error_problem
                    }
                }), 500

            type_result = predict_image(m_type, LABELS_TYPE, filepath) if m_type else None
            problem_result = predict_image(m_problem, LABELS_PROBLEM, filepath) if m_problem else None

            return jsonify({
                'success': True,
                'skin_type_analysis': type_result,
                'skin_problem_analysis': problem_result
            })

        except Exception as e:
            return jsonify({'success': False, 'message': f'Error during prediction: {str(e)}'}), 500
    
    return jsonify({'success': False, 'message': 'File type not allowed'}), 400