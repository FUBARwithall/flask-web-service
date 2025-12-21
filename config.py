import os

# Upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flutter_app'
}

# Resend configuration
RESEND_FROM_EMAIL = "noreply@pedulikulit.my.id"

# App secret key (change in production)
SECRET_KEY = 'your_secret_key_change_this_in_production'