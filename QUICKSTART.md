# 🚀 QUICK START GUIDE

Panduan cepat untuk memulai Skin Health Manager Web Dashboard.

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Setup Database
Buat database dan tabel dengan menjalankan SQL queries berikut di MySQL:

```sql
CREATE DATABASE IF NOT EXISTS flutter_app;
USE flutter_app;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skin_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skin_condition VARCHAR(255),
    severity VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## Step 3: Create Admin Account
```bash
python create_admin.py
```

Ikuti instruksi untuk membuat admin account. Contoh:
- Nama: Admin
- Email: admin@example.com
- Password: admin123

## Step 4: Run Web Service
```bash
python app.py
```

Server akan berjalan di: **http://localhost:5000/web/login**

## Step 5: Login
1. Buka browser
2. Masuk ke: http://localhost:5000/web/login
3. Gunakan email dan password yang sudah dibuat
4. Klik Login

## 🎉 Done!

Sekarang Anda bisa mengelola users dan data kulit langsung dari web interface!

---

## 📋 Features Overview

| Fitur | Deskripsi |
|-------|-----------|
| 📊 **Dashboard** | Lihat statistik dan overview |
| 👥 **Users** | Kelola users (create, read, update, delete) |
| 💊 **Skin Data** | Kelola riwayat pemeriksaan kulit |
| ⚙️ **Settings** | Ubah password admin |
| 🔐 **Security** | Session-based authentication |

---

## 💡 Tips

- **Backup Database**: Selalu backup database Anda secara berkala
- **Strong Password**: Gunakan password yang kuat untuk admin
- **HTTPS**: Gunakan HTTPS di production
- **Regular Updates**: Update dependencies secara berkala

---

## 🆘 Troubleshooting

### Port 5000 sudah digunakan?
Ubah port di `app.py` line terakhir:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Ubah 5001 dengan port pilihan
```

### MySQL tidak terkoneksi?
- Pastikan MySQL/XAMPP sedang berjalan
- Cek konfigurasi di app.py:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flutter_app'
}
```

### Template tidak ditemukan?
Pastikan struktur folder:
```
web_service/
├── app.py
├── create_admin.py
├── requirements.txt
└── templates/
    ├── base.html
    ├── web_login.html
    ├── web_dashboard.html
    ├── web_users.html
    ├── web_user_detail.html
    ├── web_skin_data.html
    └── web_settings.html
```

---

Selamat menggunakan! 🎉
