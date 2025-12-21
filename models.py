import mysql.connector
from mysql.connector import Error
import re
import random
import string
from datetime import datetime, timedelta
import resend
from config import DB_CONFIG, RESEND_FROM_EMAIL

otp_storage = {}

def get_db_connection():
    """Membuat koneksi ke database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def validate_email(email):
    """Validasi format email"""
    pattern = r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'
    return re.match(pattern, email) is not None

def generate_otp():
    """Generate 6 digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp):
    """Kirim OTP ke email menggunakan Resend - Anti-Spam Version"""
    try:
        params = {
            "from": f"Peduli Kulit <{RESEND_FROM_EMAIL}>",
            "to": [email],
            "subject": "Kode Verifikasi Akun Anda",
            "html": f'''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verifikasi Email</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="padding: 40px 40px 30px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px 12px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">Verifikasi Email Anda</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <p style="margin: 0 0 20px; color: #333333; font-size: 16px; line-height: 1.6;">
                                Halo,
                            </p>
                            <p style="margin: 0 0 30px; color: #555555; font-size: 15px; line-height: 1.6;">
                                Terima kasih telah mendaftar di <strong>Peduli Kulit</strong>. Gunakan kode verifikasi berikut untuk melanjutkan proses pendaftaran Anda:
                            </p>
                            
                            <!-- OTP Box -->
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td align="center" style="padding: 20px 0;">
                                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="background-color: #f8f9fa; border: 2px solid #667eea; border-radius: 8px; padding: 20px 40px;">
                                            <tr>
                                                <td style="text-align: center;">
                                                    <span style="font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 8px; font-family: 'Courier New', Courier, monospace;">
                                                        {otp}
                                                    </span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Info -->
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top: 30px;">
                                <tr>
                                    <td style="padding: 15px; background-color: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
                                        <p style="margin: 0; color: #856404; font-size: 14px; line-height: 1.5;">
                                            <strong>Penting:</strong> Kode ini akan kedaluwarsa dalam 5 menit. Jangan bagikan kode ini kepada siapa pun.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 30px 0 0; color: #666666; font-size: 14px; line-height: 1.6;">
                                Jika Anda tidak melakukan permintaan ini, abaikan email ini. Akun Anda tetap aman.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 30px 40px; background-color: #f8f9fa; border-top: 1px solid #e9ecef; border-radius: 0 0 12px 12px;">
                            <p style="margin: 0 0 10px; color: #6c757d; font-size: 13px; line-height: 1.5; text-align: center;">
                                Email ini dikirim secara otomatis, mohon tidak membalas.
                            </p>
                            <p style="margin: 0; color: #adb5bd; font-size: 12px; text-align: center;">
                                &copy; 2024 Peduli Kulit. Semua hak dilindungi.
                            </p>
                        </td>
                    </tr>
                    
                </table>
                
                <!-- Spam Prevention Text (Hidden but read by spam filters) -->
                <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin-top: 20px;">
                    <tr>
                        <td style="text-align: center; color: #999999; font-size: 11px; line-height: 1.4;">
                            <p style="margin: 0;">
                                Email ini dikirim ke {email} karena Anda mendaftar di layanan kami.
                            </p>
                        </td>
                    </tr>
                </table>
                
            </td>
        </tr>
    </table>
</body>
</html>
            ''',
            
            "text": f'''
Verifikasi Email Anda

Halo,

Terima kasih telah mendaftar di Peduli Kulit. Gunakan kode verifikasi berikut untuk melanjutkan proses pendaftaran Anda:

Kode Verifikasi: {otp}

PENTING: Kode ini akan kedaluwarsa dalam 5 menit. Jangan bagikan kode ini kepada siapa pun.

Jika Anda tidak melakukan permintaan ini, abaikan email ini. Akun Anda tetap aman.

---
Email ini dikirim secara otomatis, mohon tidak membalas.
© 2024 Peduli Kulit. Semua hak dilindungi.

Email ini dikirim ke {email} karena Anda mendaftar di layanan kami.
            ''',
            "headers": {
                "X-Entity-Ref-ID": f"otp-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            },
            "tags": [
                {
                    "name": "category",
                    "value": "otp_verification"
                }
            ]
        }
        
        email_response = resend.Emails.send(params)
        print(f"✅ Email sent successfully to {email}")
        print(f"Resend response: {email_response}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def allowed_file(filename):
    """Check if file extension is allowed"""
    from config import ALLOWED_EXTENSIONS
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS