# Skin Health Manager - Web Service

Web interface untuk mengelola data users dan riwayat pemeriksaan kulit tanpa perlu menggunakan phpMyAdmin.

## Features

✨ **Fitur Lengkap:**
- 🔐 Admin Login & Security
- 📊 Dashboard dengan Statistik
- 👥 Manajemen Users (CRUD)
- 💊 Manajemen Data Kulit (CRUD)
- ⚙️ Pengaturan Password Admin
- 📱 Responsive Design (Mobile & Desktop)

## Setup & Installation

### 1. Prerequisites
- Python 3.7+
- MySQL/XAMPP
- Flask & Dependencies

### 2. Install Dependencies
```bash
cd web_service
pip install -r requirements.txt
```

### 3. Database Setup
Pastikan Anda sudah membuat database dengan tabel yang diperlukan:

```sql
CREATE DATABASE flutter_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skin_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skin_condition VARCHAR(255),
    severity VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 4. Create Admin Account (First Time)
Edit `app.py` dan jalankan kode berikut di Python console untuk membuat admin:

```python
from werkzeug.security import generate_password_hash
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='flutter_app'
)

cursor = conn.cursor()
admin_password = generate_password_hash('admin123')  # Ubah dengan password yang Anda inginkan

cursor.execute(
    "INSERT INTO users (name, email, password, is_admin) VALUES (%s, %s, %s, %s)",
    ('Admin', 'admin@example.com', admin_password, True)
)

conn.commit()
cursor.close()
conn.close()

print("Admin account created successfully!")
```

### 5. Run Web Service
```bash
python app.py
```

Server akan berjalan di: `http://localhost:5000/web/login`

## Usage

### Login
1. Buka `http://localhost:5000/web/login`
2. Masukkan email dan password admin
3. Klik tombol Login

### Dashboard
Halaman utama yang menampilkan:
- Total users
- Total records kulit
- 5 user terbaru
- Statistik kondisi kulit

### Kelola Users
- Lihat semua users yang terdaftar
- Klik "Detail" untuk melihat riwayat kulit user
- Klik "Hapus" untuk menghapus user beserta data terkait

### Data Kulit
- Lihat semua riwayat pemeriksaan kulit
- Filter berdasarkan user dengan mengklik nama user
- Hapus records yang tidak diperlukan

### Pengaturan
- Ubah password admin
- Lihat informasi admin

## Project Structure

```
web_service/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── templates/
│   ├── base.html                   # Base template
│   ├── web_login.html              # Login page
│   ├── web_dashboard.html          # Dashboard
│   ├── web_users.html              # Users management
│   ├── web_user_detail.html        # User detail page
│   ├── web_skin_data.html          # Skin data management
│   └── web_settings.html           # Settings page
└── README.md                       # This file
```

## API Endpoints

### Web Interface Routes
- `GET/POST /web/login` - Login page
- `GET /web/logout` - Logout
- `GET /web/dashboard` - Dashboard (requires login)
- `GET /web/users` - Users list (requires login)
- `GET /web/users/<id>` - User detail (requires login)
- `POST /web/users/<id>/delete` - Delete user (requires login)
- `GET /web/skin-data` - Skin data list (requires login)
- `POST /web/skin-data/<id>/delete` - Delete skin record (requires login)
- `GET /web/settings` - Settings page (requires login)
- `POST /web/settings/update-password` - Update password (requires login)

### REST API Endpoints (untuk Flutter App)
- `POST /api/register` - Register user
- `POST /api/login` - Login user
- `GET /api/users/<id>` - Get user detail
- `GET /api/health` - Health check

## Security Tips

🔒 **Keamanan:**
1. Ubah `secret_key` di `app.py` untuk production
2. Gunakan password yang kuat untuk admin account
3. Jangan share password admin dengan siapa pun
4. Selalu logout setelah selesai
5. Gunakan HTTPS di production

## Troubleshooting

### Error: "Gagal terhubung ke database"
- Pastikan MySQL/XAMPP sedang berjalan
- Cek konfigurasi database di `app.py`
- Pastikan database `flutter_app` sudah dibuat

### Error: "Email atau password salah"
- Pastikan Anda login dengan account admin
- Cek database apakah user adalah admin (is_admin = 1)

### Templates not found
- Pastikan folder `templates/` berada di direktori yang sama dengan `app.py`
- Cek nama file template sudah benar

## Support

Untuk bantuan lebih lanjut, hubungi tim development.

---

**Version:** 1.0.0  
**Last Updated:** November 2025
