-- ============================================
-- SKIN HEALTH MANAGER - DATABASE SCHEMA
-- ============================================

-- Create Database
CREATE DATABASE IF NOT EXISTS flutter_app;
USE flutter_app;

-- ============================================
-- Table: users
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT 'User full name',
    email VARCHAR(255) UNIQUE NOT NULL COMMENT 'User email (unique)',
    password VARCHAR(255) NOT NULL COMMENT 'Hashed password',
    is_admin BOOLEAN DEFAULT FALSE COMMENT 'Flag: is user an admin?',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation date',
    
    -- Indexes
    INDEX idx_email (email),
    INDEX idx_is_admin (is_admin),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='User accounts table';

-- ============================================
-- Table: skin_data
-- ============================================
CREATE TABLE IF NOT EXISTS skin_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT 'Reference to users.id',
    skin_condition VARCHAR(255) COMMENT 'Type of skin condition (e.g., berjerawat, berminyak, normal)',
    severity VARCHAR(100) COMMENT 'Severity level (mild, moderate, severe)',
    notes TEXT COMMENT 'Additional notes about the condition',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation date',
    
    -- Foreign Keys
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_skin_condition (skin_condition),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Skin condition records for users';

-- ============================================
-- Table: products
-- ============================================
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    merek VARCHAR(255) NOT NULL COMMENT 'Brand name',
    nama VARCHAR(255) NOT NULL COMMENT 'Product name',
    harga DECIMAL(10,2) NOT NULL COMMENT 'Price',
    kategori_penyakit VARCHAR(255) COMMENT 'Disease category',
    image VARCHAR(500) COMMENT 'Image path or URL',
    
    -- Indexes
    INDEX idx_merek (merek),
    INDEX idx_kategori_penyakit (kategori_penyakit)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Products table';

-- ============================================
-- Sample Data for Testing
-- ============================================

-- Insert sample users (password hash for 'password123')
INSERT INTO users (name, email, password, is_admin) VALUES 
('Admin User', 'admin@example.com', 'pbkdf2:sha256:600000$...', TRUE),
('John Doe', 'john@example.com', 'pbkdf2:sha256:600000$...', FALSE),
('Jane Smith', 'jane@example.com', 'pbkdf2:sha256:600000$...', FALSE);

-- Insert sample skin data
INSERT INTO skin_data (user_id, skin_condition, severity, notes) VALUES 
(2, 'berjerawat', 'moderate', 'Jerawat di area pipi dan dahi'),
(2, 'berminyak', 'mild', 'Kulit berminyak di T-zone'),
(3, 'normal', 'mild', 'Kondisi kulit normal'),
(3, 'dermatitis_perioral', 'severe', 'Dermatitis di sekitar mulut');

-- Insert sample products
INSERT INTO products (merek, nama, harga, kategori_penyakit, image) VALUES 
('Kalpanax', 'Kalpanax Cream 10g', 18000.00, 'infeksi jamur', '🧴'),
('Canesten', 'Canesten Krim 10g', 22000.00, 'infeksi jamur', '🧴'),
('Elocon', 'Elocon Ointment 5g', 46000.00, 'eksim', '🧴'),
('Scabimite', 'Scabimite Permethrin Cream 5%', 29000.00, 'kudis', '🧴'),
('Tacrolimus', 'Tacrolimus Ointment 0.03%', 68000.00, 'vitiligo', '🧴'),
('Daivobet', 'Daivobet Gel 15g', 99000.00, 'psoriasis', '🧴'),
('Erymed', 'Erymed Gel 25ml', 28000.00, 'jerawat', '🧴'),
('Zoralin', 'Zoralin Lotion 30ml', 27000.00, 'cacar air', '🧴');

-- ============================================
-- Views (Optional - for analytics)
-- ============================================

-- View: User Statistics
CREATE OR REPLACE VIEW user_statistics AS
SELECT 
    COUNT(DISTINCT u.id) as total_users,
    COUNT(DISTINCT CASE WHEN u.is_admin = 0 THEN u.id END) as total_regular_users,
    COUNT(DISTINCT CASE WHEN u.is_admin = 1 THEN u.id END) as total_admins,
    COUNT(DISTINCT sd.id) as total_skin_records
FROM users u
LEFT JOIN skin_data sd ON u.id = sd.user_id;

-- View: Skin Condition Summary
CREATE OR REPLACE VIEW skin_condition_summary AS
SELECT 
    skin_condition,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM skin_data), 2) as percentage
FROM skin_data
WHERE skin_condition IS NOT NULL
GROUP BY skin_condition
ORDER BY count DESC;

-- View: User with Latest Skin Record
CREATE OR REPLACE VIEW user_latest_record AS
SELECT 
    u.id,
    u.name,
    u.email,
    u.created_at as user_created_at,
    sd.skin_condition,
    sd.severity,
    sd.created_at as record_created_at,
    ROW_NUMBER() OVER (PARTITION BY u.id ORDER BY sd.created_at DESC) as record_rank
FROM users u
LEFT JOIN skin_data sd ON u.id = sd.user_id;

-- ============================================
-- Useful Queries for Debugging
-- ============================================

-- Get total users
-- SELECT COUNT(*) FROM users WHERE is_admin = 0;

-- Get total skin records
-- SELECT COUNT(*) FROM skin_data;

-- Get skin conditions summary
-- SELECT skin_condition, COUNT(*) FROM skin_data GROUP BY skin_condition;

-- Get user with their latest skin record
-- SELECT u.name, u.email, MAX(sd.created_at) as latest_record
-- FROM users u
-- LEFT JOIN skin_data sd ON u.id = sd.user_id
-- WHERE u.is_admin = 0
-- GROUP BY u.id
-- ORDER BY latest_record DESC;

-- Get users with no skin records
-- SELECT u.id, u.name, u.email
-- FROM users u
-- LEFT JOIN skin_data sd ON u.id = sd.user_id
-- WHERE u.is_admin = 0 AND sd.id IS NULL;

-- ============================================
-- End of Database Schema
-- ============================================
