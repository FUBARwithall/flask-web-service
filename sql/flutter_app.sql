-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 17, 2025 at 03:21 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

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
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `id` int NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id`, `title`, `description`, `image`, `created_at`) VALUES
(1, 'Tips Merawat Kulit Berjerawat', 'Jerawat memang bikin kesal, apalagi kalau muncul pas lagi butuh tampil percaya diri. Tapi tenang, kamu bisa kok mengatasinya dengan langkah-langkah sederhana tanpa harus panik. Pertama, pastikan kamu rutin mencuci wajah dua kali sehari pakai sabun yang lembut dan sesuai jenis kulitmu. Hindari menggosok wajah terlalu keras karena bisa bikin iritasi dan memperparah jerawat. Gunakan produk non-komedogenik agar pori-pori nggak tersumbat. Kalau kamu suka pakai makeup, jangan lupa selalu bersihkan sebelum tidur, ya! Selain itu, jaga tanganmu agar nggak sering menyentuh wajah karena bakteri bisa pindah ke kulit dan menyebabkan jerawat baru. Perhatikan juga pola makan — terlalu banyak gorengan atau makanan manis bisa memicu jerawat makin parah. Perbanyak air putih dan sayur supaya kulitmu tetap sehat dari dalam. Terakhir, jangan asal coba produk skincare baru dalam waktu bersamaan, beri jeda beberapa hari untuk melihat reaksi kulitmu. Ingat, kunci utama merawat kulit berjerawat adalah sabar dan konsisten. Jerawat nggak bisa hilang semalam, tapi dengan perawatan rutin, kulitmu bisa kembali bersih dan glowing alami!', '🧴', '2025-12-10 01:06:04'),
(2, 'Pentingnya Sunscreen Setiap Hari', 'Sunscreen itu wajib banget, bukan cuma saat kamu mau ke pantai atau aktivitas di luar ruangan. Sinar UV tetap bisa menembus awan dan kaca, jadi kulitmu tetap bisa terpapar meskipun cuaca mendung atau kamu di dalam mobil.\\nDengan memakai sunscreen setiap hari, kamu bisa mencegah banyak masalah kulit seperti flek hitam, penuaan dini, dan kulit kusam. Pilih sunscreen dengan SPF minimal 30 dan PA+++ untuk perlindungan maksimal dari UVA dan UVB. Jangan lupa oleskan secara merata ke seluruh wajah dan leher sekitar 15–20 menit sebelum keluar rumah.\\nKalau kamu sering berkeringat atau beraktivitas di luar ruangan, aplikasikan ulang setiap 2–3 jam. Ada banyak jenis sunscreen sekarang—gel, cream, atau spray—jadi pilih yang paling nyaman buat kamu. Ingat, sunscreen bukan sekadar pelengkap skincare, tapi benteng utama yang melindungi kulitmu dari kerusakan jangka panjang.\\nJadi, jangan malas ya! Dengan kebiasaan kecil ini, kamu bisa menjaga kulit tetap sehat, cerah, dan awet muda lebih lama!', '☀️', '2025-12-10 01:07:38'),
(3, 'Skincare Routine untuk Pemula', 'Baru mau mulai pakai skincare tapi bingung harus dari mana? Tenang, semua orang pernah di fase itu kok! Kuncinya adalah mulai dari yang sederhana dulu. Nggak perlu langsung beli banyak produk mahal, cukup pahami kebutuhan dasar kulitmu.\\nLangkah awal yang paling penting adalah cleansing alias membersihkan wajah dua kali sehari, pagi dan malam. Setelah itu, gunakan toner untuk menyeimbangkan pH kulit. Lanjutkan dengan pelembap agar kulit tetap lembap dan sehat. Di pagi hari, tambahkan sunscreen sebagai pelindung terakhir.\\nKalau kamu sudah terbiasa, baru deh bisa pelan-pelan menambah serum atau exfoliating toner sesuai kebutuhan kulitmu. Jangan lupa, setiap orang punya jenis kulit berbeda, jadi carilah produk yang cocok buat kamu. Jangan asal ikut tren, karena skincare bukan balapan.\\nYang terpenting, konsisten! Kulit butuh waktu untuk beradaptasi. Dengan rutinitas yang teratur dan sabar, kamu bakal lihat perubahan positif di kulitmu. Ingat, perawatan kulit itu bukan tentang cepat, tapi tentang telaten.', '✨', '2025-12-10 01:07:38'),
(4, 'Mengenal Jenis Kulit Wajah', 'Sebelum beli skincare, hal pertama yang wajib kamu tahu adalah jenis kulitmu. Soalnya, salah pilih produk bisa bikin kulit iritasi, makin berminyak, atau malah kering banget.\\nSecara umum, ada lima jenis kulit wajah: normal, kering, berminyak, kombinasi, dan sensitif. Kulit normal biasanya terasa seimbang, nggak terlalu kering atau berminyak. Kulit kering cenderung terasa kaku dan bisa mengelupas di beberapa area. Kulit berminyak sering tampak mengilap dan mudah berjerawat. Kalau kombinasi, biasanya berminyak di area T-zone (dahi, hidung, dagu) tapi kering di pipi. Sedangkan kulit sensitif gampang merah dan reaktif terhadap produk tertentu.\\nCara paling mudah mengenalinya adalah dengan tes sederhana. Setelah mencuci wajah, tunggu sekitar 30 menit tanpa memakai produk apapun, lalu perhatikan bagaimana kondisi kulitmu terasa. Dari situ, kamu bisa menentukan skincare yang paling cocok.\\nDengan tahu jenis kulitmu, kamu bisa memilih produk yang tepat dan hasil perawatannya akan lebih maksimal. Jadi, kenali dulu kulitmu sebelum asal beli skincare ya!', '🔍', '2025-12-10 01:10:48'),
(5, 'Cara Memilih Moisturizer', 'Moisturizer atau pelembap adalah salah satu produk skincare yang wajib banget kamu punya. Tapi masalahnya, nggak semua pelembap cocok buat semua orang. Jadi, kamu harus tahu cara memilih yang pas untuk jenis kulitmu.\\nKalau kulitmu kering, pilih pelembap dengan tekstur cream yang mengandung bahan seperti hyaluronic acid, glycerin, atau ceramide. Bahan-bahan ini bantu menjaga kelembapan lebih lama. Untuk kulit berminyak, sebaiknya pakai pelembap berbasis gel yang ringan dan cepat meresap, biar nggak bikin wajah makin mengilap.\\nKalau kamu punya kulit sensitif, hindari produk yang mengandung alkohol atau pewangi buatan karena bisa memicu iritasi. Sedangkan kulit kombinasi bisa pakai tekstur lotion yang seimbang antara ringan dan lembap.\\nGunakan pelembap dua kali sehari setelah membersihkan wajah. Pelembap juga penting digunakan malam hari agar kulit bisa memperbaiki diri saat kamu tidur. Jadi, jangan pernah skip moisturizer karena kulit butuh ‘minuman’ juga supaya tetap sehat dan lembut.', '💧', '2025-12-10 01:10:48'),
(6, 'Manfaat Double Cleansing', 'Kamu mungkin sering dengar istilah ‘double cleansing’, tapi sebenarnya apa sih artinya? Double cleansing adalah teknik membersihkan wajah dua tahap — pertama dengan pembersih berbasis minyak, lalu dilanjutkan dengan pembersih berbasis air.\\nLangkah pertama biasanya menggunakan cleansing oil, balm, atau micellar water untuk mengangkat makeup, sunscreen, dan kotoran yang menempel seharian. Setelah itu, baru lanjut dengan sabun cuci muka (facial wash) agar kulit benar-benar bersih.\\nKenapa penting? Karena pembersihan satu tahap sering kali nggak cukup, terutama kalau kamu pakai sunscreen setiap hari. Sisa kotoran bisa menyumbat pori dan memicu jerawat. Dengan double cleansing, kulit jadi lebih siap menerima skincare berikutnya seperti toner dan serum.\\nTapi ingat, jangan berlebihan ya. Lakukan double cleansing cukup malam hari setelah beraktivitas. Di pagi hari, cukup cuci muka sekali saja agar kulit nggak kering.\\nDengan rutin melakukan double cleansing, wajahmu akan terasa lebih bersih, segar, dan bebas kusam. Kulit juga jadi lebih sehat dan glowing alami!', '🧼', '2025-12-10 01:10:48');

-- --------------------------------------------------------

--
-- Table structure for table `article_favorites`
--

CREATE TABLE `article_favorites` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `article_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `article_favorites`
--

INSERT INTO `article_favorites` (`id`, `user_id`, `article_id`, `created_at`) VALUES
(3, 1, 4, '2025-12-17 03:00:21'),
(13, 5, 4, '2025-12-17 13:40:59');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int NOT NULL,
  `merek` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Brand name',
  `nama` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Product name',
  `harga` decimal(10,2) NOT NULL COMMENT 'Price',
  `kategori_penyakit` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Disease category',
  `image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Image path or URL'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Products table';

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `merek`, `nama`, `harga`, `kategori_penyakit`, `image`) VALUES
(1, 'Kalpanax', 'Kalpanax 100 gram', 180000.00, 'Infeksi jamur', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `product_favorites`
--

CREATE TABLE `product_favorites` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `product_favorites`
--

INSERT INTO `product_favorites` (`id`, `user_id`, `product_id`, `created_at`) VALUES
(5, 5, 1, '2025-12-17 14:55:39');

-- --------------------------------------------------------

--
-- Stand-in structure for view `skin_condition_summary`
-- (See below for the actual view)
--
CREATE TABLE `skin_condition_summary` (
`count` bigint
,`percentage` decimal(26,2)
,`skin_condition` varchar(255)
);

-- --------------------------------------------------------

--
-- Table structure for table `skin_data`
--

CREATE TABLE `skin_data` (
  `id` int NOT NULL,
  `user_id` int NOT NULL COMMENT 'Reference to users.id',
  `skin_condition` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Type of skin condition (e.g., berjerawat, berminyak, normal)',
  `severity` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Severity level (mild, moderate, severe)',
  `notes` text COLLATE utf8mb4_unicode_ci COMMENT 'Additional notes about the condition',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation date'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Skin condition records for users';

--
-- Dumping data for table `skin_data`
--

INSERT INTO `skin_data` (`id`, `user_id`, `skin_condition`, `severity`, `notes`, `created_at`) VALUES
(1, 2, 'berjerawat', 'moderate', 'Jerawat di area pipi dan dahi', '2025-12-10 03:47:57'),
(2, 2, 'berminyak', 'mild', 'Kulit berminyak di T-zone', '2025-12-10 03:47:57'),
(3, 3, 'normal', 'mild', 'Kondisi kulit normal', '2025-12-10 03:47:57'),
(4, 3, 'dermatitis_perioral', 'severe', 'Dermatitis di sekitar mulut', '2025-12-10 03:47:57');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'User full name',
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'User email (unique)',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Hashed password',
  `is_admin` tinyint(1) DEFAULT '0' COMMENT 'Flag: is user an admin?',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation date'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='User accounts table';

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `is_admin`, `created_at`) VALUES
(1, 'Admin User', 'admin@example.com', 'pbkdf2:sha256:600000$...', 1, '2025-12-10 03:47:57'),
(2, 'John Doe', 'john@example.com', 'pbkdf2:sha256:600000$...', 0, '2025-12-10 03:47:57'),
(3, 'Jane Smith', 'jane@example.com', 'pbkdf2:sha256:600000$...', 0, '2025-12-10 03:47:57'),
(4, 'bintang', 'bintang@gmail.com', 'scrypt:32768:8:1$9lSWe1uhdf8N4SLK$e988c75c7eda1dda57e6e8aefadde266cb110ac37752c5d7da9b7ce2e9829595d527a06d000f9da3106b09c2a8af006796b1f0d46729643a38b36a4c91f58d84', 1, '2025-12-10 03:48:59'),
(5, 'Bintang Rafli Priatama', 'bintangrafli73@gmail.com', 'scrypt:32768:8:1$a3C3Sap3q5EkDtU0$12bf40d681e521505f7cb3d3fff9c94048a4c5c9f281dd67612419f0d07304bd4efa2c0c9329ce375ea50c62512bd0a3911a9aa6a49bd8da257cd6715faba7bd', 0, '2025-12-10 03:51:12');

-- --------------------------------------------------------

--
-- Stand-in structure for view `user_latest_record`
-- (See below for the actual view)
--
CREATE TABLE `user_latest_record` (
`email` varchar(255)
,`id` int
,`name` varchar(255)
,`record_created_at` timestamp
,`record_rank` bigint unsigned
,`severity` varchar(100)
,`skin_condition` varchar(255)
,`user_created_at` timestamp
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `user_statistics`
-- (See below for the actual view)
--
CREATE TABLE `user_statistics` (
`total_admins` bigint
,`total_regular_users` bigint
,`total_skin_records` bigint
,`total_users` bigint
);

-- --------------------------------------------------------

--
-- Structure for view `skin_condition_summary`
--
DROP TABLE IF EXISTS `skin_condition_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `skin_condition_summary`  AS SELECT `skin_data`.`skin_condition` AS `skin_condition`, count(0) AS `count`, round(((count(0) * 100.0) / (select count(0) from `skin_data`)),2) AS `percentage` FROM `skin_data` WHERE (`skin_data`.`skin_condition` is not null) GROUP BY `skin_data`.`skin_condition` ORDER BY `count` DESC ;

-- --------------------------------------------------------

--
-- Structure for view `user_latest_record`
--
DROP TABLE IF EXISTS `user_latest_record`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `user_latest_record`  AS SELECT `u`.`id` AS `id`, `u`.`name` AS `name`, `u`.`email` AS `email`, `u`.`created_at` AS `user_created_at`, `sd`.`skin_condition` AS `skin_condition`, `sd`.`severity` AS `severity`, `sd`.`created_at` AS `record_created_at`, row_number() OVER (PARTITION BY `u`.`id` ORDER BY `sd`.`created_at` desc ) AS `record_rank` FROM (`users` `u` left join `skin_data` `sd` on((`u`.`id` = `sd`.`user_id`))) ;

-- --------------------------------------------------------

--
-- Structure for view `user_statistics`
--
DROP TABLE IF EXISTS `user_statistics`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `user_statistics`  AS SELECT count(distinct `u`.`id`) AS `total_users`, count(distinct (case when (`u`.`is_admin` = 0) then `u`.`id` end)) AS `total_regular_users`, count(distinct (case when (`u`.`is_admin` = 1) then `u`.`id` end)) AS `total_admins`, count(distinct `sd`.`id`) AS `total_skin_records` FROM (`users` `u` left join `skin_data` `sd` on((`u`.`id` = `sd`.`user_id`))) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_title` (`title`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indexes for table `article_favorites`
--
ALTER TABLE `article_favorites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_article` (`user_id`,`article_id`),
  ADD KEY `article_id` (`article_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_merek` (`merek`),
  ADD KEY `idx_kategori_penyakit` (`kategori_penyakit`);

--
-- Indexes for table `product_favorites`
--
ALTER TABLE `product_favorites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_product` (`user_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `skin_data`
--
ALTER TABLE `skin_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_skin_condition` (`skin_condition`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_is_admin` (`is_admin`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `article_favorites`
--
ALTER TABLE `article_favorites`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `product_favorites`
--
ALTER TABLE `product_favorites`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `skin_data`
--
ALTER TABLE `skin_data`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `article_favorites`
--
ALTER TABLE `article_favorites`
  ADD CONSTRAINT `article_favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `article_favorites_ibfk_2` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_favorites`
--
ALTER TABLE `product_favorites`
  ADD CONSTRAINT `product_favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_favorites_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `skin_data`
--
ALTER TABLE `skin_data`
  ADD CONSTRAINT `skin_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
