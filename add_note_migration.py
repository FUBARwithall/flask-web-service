import mysql.connector
from config import DB_CONFIG

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Add note column to face_analyses
    cursor.execute("""
        ALTER TABLE face_analyses 
        ADD COLUMN note TEXT NULL
    """)
    print("✅ Added note column to face_analyses")
    
    # Add note column to body_analyses
    cursor.execute("""
        ALTER TABLE body_analyses 
        ADD COLUMN note TEXT NULL
    """)
    print("✅ Added note column to body_analyses")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Migration completed successfully!")
    
except mysql.connector.Error as e:
    if "Duplicate column name" in str(e):
        print("⚠️ Note column already exists, skipping...")
    else:
        print(f"❌ Error: {e}")
