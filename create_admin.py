#!/usr/bin/env python3
"""
Script untuk membuat admin account untuk pertama kali
Run: python create_admin.py
"""

import mysql.connector
from werkzeug.security import generate_password_hash

def create_admin():
    print("=" * 50)
    print("SKIN HEALTH MANAGER - CREATE ADMIN ACCOUNT")
    print("=" * 50)
    
    # Get input
    name = input("\nMasukkan nama admin: ").strip()
    email = input("Masukkan email admin: ").strip().lower()
    password = input("Masukkan password admin (minimal 6 karakter): ").strip()
    
    # Validate
    if not name:
        print("❌ Error: Nama tidak boleh kosong!")
        return
    
    if not email or '@' not in email:
        print("❌ Error: Email tidak valid!")
        return
    
    if len(password) < 6:
        print("❌ Error: Password minimal 6 karakter!")
        return
    
    # Connect to database
    try:
        print("\n⏳ Menghubungkan ke database...")
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='flutter_app'
        )
        cursor = conn.cursor(dictionary=True)
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"❌ Error: Email '{email}' sudah terdaftar!")
            cursor.close()
            conn.close()
            return
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Insert admin
        cursor.execute(
            "INSERT INTO users (name, email, password, is_admin) VALUES (%s, %s, %s, %s)",
            (name, email, hashed_password, True)
        )
        conn.commit()
        
        admin_id = cursor.lastrowid
        
        print("\n" + "=" * 50)
        print("✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!")
        print("=" * 50)
        print(f"ID: #{admin_id}")
        print(f"Nama: {name}")
        print(f"Email: {email}")
        print(f"Password: {'*' * len(password)}")
        print("=" * 50)
        print("\n✨ Anda sekarang bisa login ke:")
        print("   http://localhost:5000/web/login")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database Error: {e}")
        print("Pastikan MySQL/XAMPP sudah berjalan dan database 'flutter_app' sudah dibuat.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    create_admin()
