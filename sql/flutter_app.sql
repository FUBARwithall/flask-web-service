-- Comprehensive Database Migration Script v1.0
-- This script sets up the entire database structure for the Skin Health Manager application.

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------
-- 1. BASE TABLES (No dependencies)
-- --------------------------------------------------------

-- Table: users
CREATE TABLE IF NOT EXISTS `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `is_admin` tinyint (1) DEFAULT 0,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp (),
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`),
    KEY `idx_email` (`email`),
    KEY `idx_is_admin` (`is_admin`),
    KEY `idx_created_at` (`created_at`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Table: articles
CREATE TABLE IF NOT EXISTS `articles` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    `description` longtext NOT NULL,
    `image` varchar(255) DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp (),
    PRIMARY KEY (`id`),
    KEY `idx_title` (`title`),
    KEY `idx_created_at` (`created_at`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- Table: products
CREATE TABLE IF NOT EXISTS `products` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `merek` varchar(255) NOT NULL,
    `nama` varchar(255) NOT NULL,
    `harga` decimal(10, 2) NOT NULL,
    `kategori_penyakit` varchar(255) DEFAULT NULL,
    `image` varchar(500) DEFAULT NULL,
    `deskripsi` text DEFAULT NULL,
    `dosis` varchar(255) DEFAULT NULL,
    `efek_samping` varchar(255) DEFAULT NULL,
    `komposisi` text DEFAULT NULL,
    `manufaktur` varchar(255) DEFAULT NULL,
    `nomor_registrasi` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Table: foods
CREATE TABLE IF NOT EXISTS `foods` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `oil` tinyint (4) NOT NULL COMMENT '0–4 minyak/gorengan',
    `simple_carb` tinyint (4) NOT NULL COMMENT '0–4 karbo sederhana',
    `sugar` tinyint (4) NOT NULL COMMENT '0–4 gula',
    `fiber` tinyint (4) NOT NULL COMMENT '0–4 serat',
    `fermented` tinyint (4) NOT NULL COMMENT '0–4 fermentasi',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- Table: drinks
CREATE TABLE IF NOT EXISTS `drinks` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `drink_type` enum ('WATER', 'SWEET') NOT NULL,
    `sugar` tinyint (4) DEFAULT 0,
    PRIMARY KEY (`id`),
    KEY `idx_drink_type` (`drink_type`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------
-- 2. DEPENDENT TABLES (Require Base Tables)
-- --------------------------------------------------------

-- Table: skin_data
CREATE TABLE IF NOT EXISTS `skin_data` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `skin_condition` varchar(255) DEFAULT NULL,
    `severity` varchar(100) DEFAULT NULL,
    `notes` text DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp (),
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_skin_condition` (`skin_condition`),
    KEY `idx_created_at` (`created_at`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Table: daily_skin_analysis
CREATE TABLE IF NOT EXISTS `daily_skin_analysis` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `log_date` date NOT NULL,
    `total_oil` float NOT NULL,
    `total_simple_carb` float NOT NULL,
    `total_sugar` float NOT NULL,
    `total_fiber` float NOT NULL,
    `total_fermented` float NOT NULL,
    `hydration` float NOT NULL,
    `sleep_deficit` float NOT NULL,
    `skin_load_score` float NOT NULL,
    `status` enum ('AMAN', 'WASPADA', 'OVER_LIMIT') NOT NULL,
    `main_triggers` text DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp (),
    PRIMARY KEY (`id`),
    KEY `fk_analysis_user` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- Table: daily_food_logs
CREATE TABLE IF NOT EXISTS `daily_food_logs` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `food_id` int(11) NOT NULL,
    `quantity` int(11) NOT NULL,
    `log_date` date NOT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_food_user` (`user_id`),
    KEY `fk_food_food` (`food_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- Table: daily_drink_logs
CREATE TABLE IF NOT EXISTS `daily_drink_logs` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `drink_id` int(11) NOT NULL,
    `quantity` int(11) NOT NULL,
    `log_date` date NOT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_drink_user` (`user_id`),
    KEY `fk_drink_drink` (`drink_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- Table: daily_sleep_logs
CREATE TABLE IF NOT EXISTS `daily_sleep_logs` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `log_date` date NOT NULL,
    `sleep_hours` float NOT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_sleep_user` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- Table: article_favorites
CREATE TABLE IF NOT EXISTS `article_favorites` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `article_id` int(11) NOT NULL,
    `created_at` timestamp NULL DEFAULT current_timestamp (),
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Table: product_favorites
CREATE TABLE IF NOT EXISTS `product_favorites` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `product_id` int(11) NOT NULL,
    `created_at` timestamp NULL DEFAULT current_timestamp (),
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Table: face_analyses
CREATE TABLE IF NOT EXISTS `face_analyses` (
    `id` varchar(36) NOT NULL,
    `user_id` int(11) NOT NULL,
    `timestamp` varchar(30) DEFAULT NULL,
    `image_filename` varchar(255) DEFAULT NULL,
    `image_url` varchar(255) DEFAULT NULL,
    `skin_type` varchar(50) DEFAULT NULL,
    `skin_type_confidence` float DEFAULT NULL,
    `skin_type_predictions` json DEFAULT NULL,
    `skin_problem` varchar(50) DEFAULT NULL,
    `skin_problem_confidence` float DEFAULT NULL,
    `skin_problem_predictions` json DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_face_user` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------
-- 3. FOREIGN KEYS (Added after all tables are created)
-- --------------------------------------------------------

ALTER TABLE `daily_drink_logs`
  ADD CONSTRAINT `fk_drink_drink` FOREIGN KEY (`drink_id`) REFERENCES `drinks` (`id`),
  ADD CONSTRAINT `fk_drink_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `daily_food_logs`
  ADD CONSTRAINT `fk_food_food` FOREIGN KEY (`food_id`) REFERENCES `foods` (`id`),
  ADD CONSTRAINT `fk_food_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `daily_skin_analysis`
  ADD CONSTRAINT `fk_analysis_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `daily_sleep_logs`
  ADD CONSTRAINT `fk_sleep_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `skin_data`
  ADD CONSTRAINT `skin_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `face_analyses`
  ADD CONSTRAINT `fk_face_analysis_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `article_favorites`
  ADD CONSTRAINT `fk_fav_article` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_fav_user_article` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `product_favorites`
  ADD CONSTRAINT `fk_fav_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_fav_user_product` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
