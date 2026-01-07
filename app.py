from flask import Flask, jsonify
from flask_cors import CORS
import resend
import os
from config import SECRET_KEY, UPLOAD_FOLDER, RESEND_FROM_EMAIL
from flask_jwt_extended import JWTManager

resend.api_key = 're_G81rJoda_4yAmyTMaqdbbh9R58nt8U6ty'

app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app)

# JWT CONFIG (WAJIB)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    print(f"DEBUG JWT: Unauthorized - {callback}")
    return jsonify({'status': 'error', 'message': 'Missing Authorization Header', 'debug': callback}), 401

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    print(f"DEBUG JWT: Invalid Token - {callback}")
    return jsonify({'status': 'error', 'message': 'Invalid Token', 'debug': callback}), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print(f"DEBUG JWT: Expired Token")
    return jsonify({'status': 'error', 'message': 'Token Expired'}), 401

# Upload config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Register blueprints
from auth import auth_bp
from articles import articles_bp
from products import products_bp
from daily_logs import daily_logs_bp
from web_admin import web_admin_bp
from chatbot import chatbot_bp

app.register_blueprint(auth_bp)
app.register_blueprint(articles_bp)
app.register_blueprint(products_bp)
app.register_blueprint(daily_logs_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(web_admin_bp, url_prefix='/web')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
