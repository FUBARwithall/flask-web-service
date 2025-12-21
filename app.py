from flask import Flask
from flask_cors import CORS
import resend
import os
from config import SECRET_KEY, UPLOAD_FOLDER, RESEND_FROM_EMAIL

# Initialize Resend
resend.api_key = 're_G81rJoda_4yAmyTMaqdbbh9R58nt8U6ty'

# Create Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app)

# Upload configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Register blueprints
from auth import auth_bp
from articles import articles_bp
from products import products_bp
from web_admin import web_admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(articles_bp)
app.register_blueprint(products_bp)
app.register_blueprint(web_admin_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
