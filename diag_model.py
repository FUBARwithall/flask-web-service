import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_TYPE_PATH = os.path.join(BASE_DIR, 'ml_models', 'model_jeniskulit.keras')
MODEL_PROBLEM_PATH = os.path.join(BASE_DIR, 'ml_models', 'model_masalah_kulit.keras')

print(f"Python Version: {sys.version}")
print(f"Current Directory: {os.getcwd()}")
print(f"Base Dir: {BASE_DIR}")
print(f"Looking for Type Model at: {MODEL_TYPE_PATH}")
print(f"Exists? {os.path.exists(MODEL_TYPE_PATH)}")
print(f"Looking for Problem Model at: {MODEL_PROBLEM_PATH}")
print(f"Exists? {os.path.exists(MODEL_PROBLEM_PATH)}")

try:
    import tensorflow as tf
    import numpy as np
    print(f"TensorFlow Version: {tf.__version__}")
    
    print("\n--- Testing Type Model ---")
    if os.path.exists(MODEL_TYPE_PATH):
        m_type = tf.keras.models.load_model(MODEL_TYPE_PATH, compile=False)
        print("✅ Successfully loaded Type Model")
        # Test with dummy data
        dummy_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
        pred = m_type.predict(dummy_input, verbose=0)
        print(f"✅ Prediction Test Success: Shape {pred.shape}")
        print(f"   Values: {pred[0]}")
    else:
        print("❌ Type Model file not found")

    print("\n--- Testing Problem Model ---")
    if os.path.exists(MODEL_PROBLEM_PATH):
        m_problem = tf.keras.models.load_model(MODEL_PROBLEM_PATH, compile=False)
        print("✅ Successfully loaded Problem Model")
        # Test with dummy data
        dummy_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
        pred = m_problem.predict(dummy_input, verbose=0)
        print(f"✅ Prediction Test Success: Shape {pred.shape}")
        print(f"   Values: {pred[0]}")
    else:
        print("❌ Problem Model file not found")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
