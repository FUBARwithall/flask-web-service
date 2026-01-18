-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 18 Jan 2026 pada 11.52
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flutter_app`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `article_favorites`
--

CREATE TABLE `article_favorites` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `body_analyses`
--

CREATE TABLE `body_analyses` (
  `id` varchar(36) NOT NULL,
  `user_id` int(11) NOT NULL,
  `timestamp` varchar(30) DEFAULT NULL,
  `image_filename` varchar(255) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `disease_key` varchar(50) DEFAULT NULL,
  `disease_name` varchar(100) DEFAULT NULL,
  `confidence` float DEFAULT NULL,
  `all_predictions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`all_predictions`)),
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `conversations`
--

CREATE TABLE `conversations` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT 'Chat Baru',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `daily_drink_logs`
--

CREATE TABLE `daily_drink_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `drink_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL COMMENT 'gelas / botol',
  `log_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `daily_food_logs`
--

CREATE TABLE `daily_food_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `food_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL COMMENT 'berapa kali/porsi',
  `log_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `daily_skin_analysis`
--

CREATE TABLE `daily_skin_analysis` (
  `id` int(11) NOT NULL,
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
  `status` enum('AMAN','WASPADA','OVER_LIMIT') NOT NULL,
  `main_triggers` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `daily_sleep_logs`
--

CREATE TABLE `daily_sleep_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `log_date` date NOT NULL,
  `sleep_hours` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `drinks`
--

CREATE TABLE `drinks` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `drink_type` enum('WATER','SWEET') NOT NULL,
  `sugar` tinyint(4) DEFAULT 0 COMMENT '0–4 gula per unit'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `face_analyses`
--

CREATE TABLE `face_analyses` (
  `id` varchar(36) NOT NULL,
  `user_id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `image_filename` varchar(255) NOT NULL,
  `image_url` varchar(500) NOT NULL,
  `skin_type` varchar(20) NOT NULL,
  `skin_type_confidence` float NOT NULL,
  `skin_type_predictions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`skin_type_predictions`)),
  `skin_problem` varchar(20) NOT NULL,
  `skin_problem_confidence` float NOT NULL,
  `skin_problem_predictions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`skin_problem_predictions`)),
  `created_at` datetime DEFAULT current_timestamp(),
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `foods`
--

CREATE TABLE `foods` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `oil` tinyint(4) NOT NULL COMMENT '0–4 minyak/gorengan',
  `simple_carb` tinyint(4) NOT NULL COMMENT '0–4 karbo sederhana',
  `sugar` tinyint(4) NOT NULL COMMENT '0–4 gula',
  `fiber` tinyint(4) NOT NULL COMMENT '0–4 serat',
  `fermented` tinyint(4) NOT NULL COMMENT '0–4 fermentasi'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `conversation_id` int(11) NOT NULL,
  `role` enum('user','assistant') NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `merek` varchar(255) NOT NULL COMMENT 'Brand name',
  `nama` varchar(255) NOT NULL COMMENT 'Product name',
  `harga` decimal(10,2) NOT NULL COMMENT 'Price',
  `kategori_penyakit` varchar(255) DEFAULT NULL COMMENT 'Disease category',
  `image` varchar(500) DEFAULT NULL COMMENT 'Image path or URL',
  `deskripsi` text DEFAULT NULL COMMENT 'Product description',
  `dosis` varchar(255) DEFAULT NULL COMMENT 'Dosage instructions',
  `efek_samping` varchar(255) DEFAULT NULL COMMENT 'Side effects',
  `komposisi` text DEFAULT NULL COMMENT 'Product composition',
  `manufaktur` varchar(255) DEFAULT NULL COMMENT 'Manufacturer',
  `nomor_registrasi` varchar(255) DEFAULT NULL COMMENT 'Registration number'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Products table';

-- --------------------------------------------------------

--
-- Struktur dari tabel `product_comments`
--

CREATE TABLE `product_comments` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment` text NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `parent_id` int(11) DEFAULT NULL,
  `sentiment` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `product_favorites`
--

CREATE TABLE `product_favorites` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `skin_data`
--

CREATE TABLE `skin_data` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL COMMENT 'Reference to users.id',
  `skin_condition` varchar(255) DEFAULT NULL COMMENT 'Type of skin condition (e.g., berjerawat, berminyak, normal)',
  `severity` varchar(100) DEFAULT NULL COMMENT 'Severity level (mild, moderate, severe)',
  `notes` text DEFAULT NULL COMMENT 'Additional notes about the condition',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'Record creation date'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Skin condition records for users';

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL COMMENT 'User full name',
  `email` varchar(255) NOT NULL COMMENT 'User email (unique)',
  `password` varchar(255) NOT NULL COMMENT 'Hashed password',
  `is_admin` tinyint(1) DEFAULT 0 COMMENT 'Flag: is user an admin?',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'Account creation date'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='User accounts table';

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_title` (`title`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indeks untuk tabel `body_analyses`
--
ALTER TABLE `body_analyses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `conversations`
--
ALTER TABLE `conversations`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `daily_drink_logs`
--
ALTER TABLE `daily_drink_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_drink_user` (`user_id`),
  ADD KEY `fk_drink_drink` (`drink_id`);

--
-- Indeks untuk tabel `daily_food_logs`
--
ALTER TABLE `daily_food_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_food_user` (`user_id`),
  ADD KEY `fk_food_food` (`food_id`);

--
-- Indeks untuk tabel `daily_skin_analysis`
--
ALTER TABLE `daily_skin_analysis`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_analysis_user` (`user_id`);

--
-- Indeks untuk tabel `daily_sleep_logs`
--
ALTER TABLE `daily_sleep_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_sleep_user` (`user_id`);

--
-- Indeks untuk tabel `drinks`
--
ALTER TABLE `drinks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_drink_type` (`drink_type`);

--
-- Indeks untuk tabel `face_analyses`
--
ALTER TABLE `face_analyses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_timestamp` (`user_id`,`timestamp`);

--
-- Indeks untuk tabel `foods`
--
ALTER TABLE `foods`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `conversation_id` (`conversation_id`);

--
-- Indeks untuk tabel `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `product_comments`
--
ALTER TABLE `product_comments`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `skin_data`
--
ALTER TABLE `skin_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_skin_condition` (`skin_condition`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_is_admin` (`is_admin`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `conversations`
--
ALTER TABLE `conversations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `daily_drink_logs`
--
ALTER TABLE `daily_drink_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `daily_food_logs`
--
ALTER TABLE `daily_food_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `daily_skin_analysis`
--
ALTER TABLE `daily_skin_analysis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `daily_sleep_logs`
--
ALTER TABLE `daily_sleep_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `drinks`
--
ALTER TABLE `drinks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `foods`
--
ALTER TABLE `foods`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `product_comments`
--
ALTER TABLE `product_comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `skin_data`
--
ALTER TABLE `skin_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `body_analyses`
--
ALTER TABLE `body_analyses`
  ADD CONSTRAINT `body_analyses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ketidakleluasaan untuk tabel `daily_drink_logs`
--
ALTER TABLE `daily_drink_logs`
  ADD CONSTRAINT `fk_drink_drink` FOREIGN KEY (`drink_id`) REFERENCES `drinks` (`id`),
  ADD CONSTRAINT `fk_drink_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ketidakleluasaan untuk tabel `daily_food_logs`
--
ALTER TABLE `daily_food_logs`
  ADD CONSTRAINT `fk_food_food` FOREIGN KEY (`food_id`) REFERENCES `foods` (`id`),
  ADD CONSTRAINT `fk_food_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ketidakleluasaan untuk tabel `daily_skin_analysis`
--
ALTER TABLE `daily_skin_analysis`
  ADD CONSTRAINT `fk_analysis_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ketidakleluasaan untuk tabel `daily_sleep_logs`
--
ALTER TABLE `daily_sleep_logs`
  ADD CONSTRAINT `fk_sleep_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ketidakleluasaan untuk tabel `face_analyses`
--
ALTER TABLE `face_analyses`
  ADD CONSTRAINT `face_analyses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `skin_data`
--
ALTER TABLE `skin_data`
  ADD CONSTRAINT `skin_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
