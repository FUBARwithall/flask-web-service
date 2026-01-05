from flask import Blueprint, request, jsonify
from huggingface_hub import hf_hub_download
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os

api_bp = Blueprint("api", __name__, url_prefix="/api")

# ===== LOAD MODEL SEKALI =====
MODEL_REPO = "nitisasmita/model_jeniskulit"
MODEL_FILE = "model_jeniskulit.keras"

model_path = hf_hub_download(
    repo_id=MODEL_REPO, 
    filename=MODEL_FILE, 
    token=os.getenv("HFJK_TOKEN")
)

model = tf.keras.models.load_model(model_path)
print("✅ Model loaded")

CLASS_NAMES = ["berminyak", "kering", "normal"]

def preprocess(img):
    # 1. Konversi PIL Image ke format OpenCV (numpy array)
    img_np = np.array(img)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    # 2. Handling Sinar UV: Gunakan Grayscale + CLAHE
    # Mempertajam tekstur agar flek/minyak terlihat jelas meski difoto dengan UV
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # 3. Kembali ke 3 channel (RGB) untuk input MobileNetV2
    final_img = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
    
    # 4. Resize & Normalize
    final_img = cv2.resize(final_img, (224, 224))
    final_img = final_img / 255.0
    final_img = np.expand_dims(final_img, axis=0)
    return final_img

@api_bp.route("/ping", methods=["GET"])
def ping():
    return {"status": "ok"}

@api_bp.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        # Buka gambar
        image = Image.open(request.files["image"]).convert("RGB")
        
        # Preprocessing
        x = preprocess(image)

        # Prediksi
        preds = model.predict(x)[0]
        idx = int(np.argmax(preds))
        label = CLASS_NAMES[idx]

        return jsonify({
            "status": "success",
            "prediction": {
                "class": label,
                "confidence": round(float(preds[idx]) * 100, 2)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500