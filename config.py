import os

# Upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'flutter_app')
}

# Resend configuration
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "noreply@pedulikulit.my.id")

# App secret key
SECRET_KEY = os.getenv('SECRET_KEY', 'default-unsecure-key-for-local-dev-only')