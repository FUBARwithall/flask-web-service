-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 24 Des 2025 pada 05.34
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

--
-- Dumping data untuk tabel `articles`
--

INSERT INTO `articles` (`id`, `title`, `description`, `image`, `created_at`) VALUES
(1, 'Tips Merawat Kulit Berjerawat', '<p>Jerawat memang bikin kesal, apalagi kalau muncul pas lagi butuh tampil percaya diri.</p>\r\n<p>Tapi tenang, kamu bisa kok mengatasinya dengan langkah-langkah sederhana tanpa harus panik.</p>\r\n<p>Pertama, pastikan kamu rutin mencuci wajah dua kali sehari pakai sabun yang lembut dan sesuai jenis kulitmu. Hindari menggosok wajah terlalu keras karena bisa bikin iritasi dan memperparah jerawat.</p>\r\n<p>Gunakan produk non-komedogenik agar pori-pori nggak tersumbat. Kalau kamu suka pakai makeup, jangan lupa selalu bersihkan sebelum tidur, ya!</p>\r\n<p>Selain itu, jaga tanganmu agar nggak sering menyentuh wajah karena bakteri bisa pindah ke kulit dan menyebabkan jerawat baru.</p>\r\n<p>Perhatikan juga pola makan &mdash; terlalu banyak gorengan atau makanan manis bisa memicu jerawat makin parah. Perbanyak air putih dan sayur supaya kulitmu tetap sehat dari dalam.</p>\r\n<p>Terakhir, jangan asal coba produk skincare baru dalam waktu bersamaan, beri jeda beberapa hari untuk melihat reaksi kulitmu. Ingat, kunci utama merawat kulit berjerawat adalah sabar dan konsisten.</p>\r\n<p>Jerawat nggak bisa hilang semalam, tapi dengan perawatan rutin, kulitmu bisa kembali bersih dan glowing alami!</p>', '20251223_210703_hoi4-gdr-keyart-loop-frame.jpg', '2025-12-10 01:06:04'),
(2, 'Pentingnya Sunscreen Setiap Hari', '<p>Sunscreen itu wajib banget, bukan cuma saat kamu mau ke pantai atau aktivitas di luar ruangan. Sinar UV tetap bisa menembus awan dan kaca, jadi kulitmu tetap bisa terpapar meskipun cuaca mendung atau kamu di dalam mobil.</p>\r\n<p>Dengan memakai sunscreen setiap hari, kamu bisa mencegah banyak masalah kulit seperti flek hitam, penuaan dini, dan kulit kusam. Pilih sunscreen dengan SPF minimal 30 dan PA+++ untuk perlindungan maksimal dari UVA dan UVB. Jangan lupa oleskan secara merata ke seluruh wajah dan leher sekitar 15&ndash;20 menit sebelum keluar rumah.</p>\r\n<p>Kalau kamu sering berkeringat atau beraktivitas di luar ruangan, aplikasikan ulang setiap 2&ndash;3 jam. Ada banyak jenis sunscreen sekarang&mdash;gel, cream, atau spray&mdash;jadi pilih yang paling nyaman buat kamu. Ingat, sunscreen bukan sekadar pelengkap skincare, tapi benteng utama yang melindungi kulitmu dari kerusakan jangka panjang.</p>\r\n<p>Jadi, jangan malas ya! Dengan kebiasaan kecil ini, kamu bisa menjaga kulit tetap sehat, cerah, dan awet muda lebih lama!</p>', '20251223_210647_Kaga.jpg', '2025-12-10 01:07:38'),
(3, 'Skincare Routine untuk Pemula', '<p>Baru mau mulai pakai skincare tapi bingung harus dari mana? Tenang, semua orang pernah di fase itu kok! Kuncinya adalah mulai dari yang sederhana dulu. Nggak perlu langsung beli banyak produk mahal, cukup pahami kebutuhan dasar kulitmu.</p>\r\n<p>Langkah awal yang paling penting adalah cleansing alias membersihkan wajah dua kali sehari, pagi dan malam. Setelah itu, gunakan toner untuk menyeimbangkan pH kulit. Lanjutkan dengan pelembap agar kulit tetap lembap dan sehat. Di pagi hari, tambahkan sunscreen sebagai pelindung terakhir.</p>\r\n<p>Kalau kamu sudah terbiasa, baru deh bisa pelan-pelan menambah serum atau exfoliating toner sesuai kebutuhan kulitmu. Jangan lupa, setiap orang punya jenis kulit berbeda, jadi carilah produk yang cocok buat kamu. Jangan asal ikut tren, karena skincare bukan balapan.</p>\r\n<p>Yang terpenting, konsisten! Kulit butuh waktu untuk beradaptasi. Dengan rutinitas yang teratur dan sabar, kamu bakal lihat perubahan positif di kulitmu. Ingat, perawatan kulit itu bukan tentang cepat, tapi tentang telaten.</p>', '20251223_210654_photo.png', '2025-12-10 01:07:38'),
(4, 'Mengenal Jenis Kulit Wajah', '<p>Sebelum beli skincare, hal pertama yang wajib kamu tahu adalah jenis kulitmu. Soalnya, salah pilih produk bisa bikin kulit iritasi, makin berminyak, atau malah kering banget.</p>\r\n<p>Secara umum, ada lima jenis kulit wajah: normal, kering, berminyak, kombinasi, dan sensitif. Kulit normal biasanya terasa seimbang, nggak terlalu kering atau berminyak. Kulit kering cenderung terasa kaku dan bisa mengelupas di beberapa area. Kulit berminyak sering tampak mengilap dan mudah berjerawat. Kalau kombinasi, biasanya berminyak di area T-zone (dahi, hidung, dagu) tapi kering di pipi. Sedangkan kulit sensitif gampang merah dan reaktif terhadap produk tertentu.</p>\r\n<p>Cara paling mudah mengenalinya adalah dengan tes sederhana. Setelah mencuci wajah, tunggu sekitar 30 menit tanpa memakai produk apapun, lalu perhatikan bagaimana kondisi kulitmu terasa. Dari situ, kamu bisa menentukan skincare yang paling cocok.</p>\r\n<p>Dengan tahu jenis kulitmu, kamu bisa memilih produk yang tepat dan hasil perawatannya akan lebih maksimal. Jadi, kenali dulu kulitmu sebelum asal beli skincare yah!</p>', '20251222_101942_alamak.jpg', '2025-12-10 01:10:48'),
(5, 'Cara Memilih Moisturizer', '<p>Moisturizer atau pelembap adalah salah satu produk skincare yang wajib banget kamu punya. Tapi masalahnya, nggak semua pelembap cocok buat semua orang. Jadi, kamu harus tahu cara memilih yang pas untuk jenis kulitmu.</p>\r\n<p>Kalau kulitmu kering, pilih pelembap dengan tekstur cream yang mengandung bahan seperti hyaluronic acid, glycerin, atau ceramide. Bahan-bahan ini bantu menjaga kelembapan lebih lama. Untuk kulit berminyak, sebaiknya pakai pelembap berbasis gel yang ringan dan cepat meresap, biar nggak bikin wajah makin mengilap.</p>\r\n<p>Kalau kamu punya kulit sensitif, hindari produk yang mengandung alkohol atau pewangi buatan karena bisa memicu iritasi. Sedangkan kulit kombinasi bisa pakai tekstur lotion yang seimbang antara ringan dan lembap.</p>\r\n<p>Gunakan pelembap dua kali sehari setelah membersihkan wajah. Pelembap juga penting digunakan malam hari agar kulit bisa memperbaiki diri saat kamu tidur. Jadi, jangan pernah skip moisturizer karena kulit butuh &lsquo;minuman&rsquo; juga supaya tetap sehat dan lembut.</p>', '20251213_224431_download.jpeg', '2025-12-10 01:10:48'),
(6, 'Manfaat Double Cleansing', '<p>Kamu mungkin sering dengar istilah \'double cleansing\', tapi sebenarnya apa sih artinya? Double cleansing adalah teknik membersihkan wajah dua tahap &mdash; pertama dengan pembersih berbasis minyak, lalu dilanjutkan dengan pembersih berbasis air.</p>\r\n<p>Langkah pertama biasanya menggunakan cleansing oil, balm, atau micellar water untuk mengangkat makeup, sunscreen, dan kotoran yang menempel seharian. Setelah itu, baru lanjut dengan sabun cuci muka (facial wash) agar kulit benar-benar bersih.</p>\r\n<p>Kenapa penting? Karena pembersihan satu tahap sering kali nggak cukup, terutama kalau kamu pakai sunscreen setiap hari. Sisa kotoran bisa menyumbat pori dan memicu jerawat. Dengan double cleansing, kulit jadi lebih siap menerima skincare berikutnya seperti toner dan serum.</p>\r\n<p>Tapi ingat, jangan berlebihan ya. Lakukan double cleansing cukup malam hari setelah beraktivitas. Di pagi hari, cukup cuci muka sekali saja agar kulit nggak kering.</p>\r\n<p>Dengan rutin melakukan double cleansing, wajahmu akan terasa lebih bersih, segar, dan bebas kusam. Kulit juga jadi lebih sehat dan glowing alami!</p>', '20251213_224437_images.jpeg', '2025-12-10 01:10:48');

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

--
-- Dumping data untuk tabel `article_favorites`
--

INSERT INTO `article_favorites` (`id`, `user_id`, `article_id`, `created_at`) VALUES
(0, 4, 4, '2025-12-18 12:04:00'),
(0, 8, 2, '2025-12-23 14:08:51');

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

--
-- Dumping data untuk tabel `daily_drink_logs`
--

INSERT INTO `daily_drink_logs` (`id`, `user_id`, `drink_id`, `quantity`, `log_date`) VALUES
(1, 1, 2, 5, '2025-12-22'),
(2, 1, 7, 1, '2025-12-22'),
(3, 1, 1, 1, '2025-12-24');

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

--
-- Dumping data untuk tabel `daily_food_logs`
--

INSERT INTO `daily_food_logs` (`id`, `user_id`, `food_id`, `quantity`, `log_date`) VALUES
(1, 1, 3, 1, '2025-12-22'),
(2, 1, 2, 1, '2025-12-22'),
(3, 1, 1, 2, '2025-12-22'),
(4, 1, 3, 1, '2025-12-24');

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

--
-- Dumping data untuk tabel `daily_skin_analysis`
--

INSERT INTO `daily_skin_analysis` (`id`, `user_id`, `log_date`, `total_oil`, `total_simple_carb`, `total_sugar`, `total_fiber`, `total_fermented`, `hydration`, `sleep_deficit`, `skin_load_score`, `status`, `main_triggers`, `created_at`) VALUES
(1, 1, '2025-12-22', 66, 42, 6, 12, 12, 54, 0, 88, 'OVER_LIMIT', 'Konsumsi minyak/gorengan berlebih; Konsumsi karbohidrat sederhana tinggi', '2025-12-22 11:45:29'),
(2, 3, '2025-12-24', 4, 1, 0, 0, 0, 1, 0.5, 5.25, 'WASPADA', 'Serat kurang; Hidrasi kurang', '2025-12-24 03:55:12');

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

--
-- Dumping data untuk tabel `daily_sleep_logs`
--

INSERT INTO `daily_sleep_logs` (`id`, `user_id`, `log_date`, `sleep_hours`) VALUES
(1, 1, '2025-01-10', 5),
(2, 1, '2025-12-22', 8),
(3, 1, '2025-12-22', 8),
(4, 1, '2025-12-22', 8),
(5, 1, '2025-12-24', 7.5);

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

--
-- Dumping data untuk tabel `drinks`
--

INSERT INTO `drinks` (`id`, `name`, `drink_type`, `sugar`) VALUES
(1, 'Air Putih', 'WATER', 0),
(2, 'Air Mineral', 'WATER', 0),
(3, 'Teh Manis', 'SWEET', 3),
(4, 'Kopi Susu', 'SWEET', 2),
(5, 'Jus Jeruk', 'SWEET', 4),
(6, 'Soda', 'SWEET', 5),
(7, 'Es Teh Tawar', 'WATER', 0),
(8, 'Teh Hijau', 'WATER', 0);

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

--
-- Dumping data untuk tabel `foods`
--

INSERT INTO `foods` (`id`, `name`, `oil`, `simple_carb`, `sugar`, `fiber`, `fermented`) VALUES
(1, 'Tempe Goreng', 2, 1, 0, 1, 1),
(2, 'Nasi Goreng', 3, 4, 1, 0, 0),
(3, 'Ayam Goreng', 4, 1, 0, 0, 0);

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

--
-- Dumping data untuk tabel `products`
--

INSERT INTO `products` (`id`, `merek`, `nama`, `harga`, `kategori_penyakit`, `image`, `deskripsi`, `dosis`, `efek_samping`, `komposisi`, `manufaktur`, `nomor_registrasi`) VALUES
(0, 'Kalpanax', 'Kalpanax Cream 5g', 20000.00, 'infeksi jamur', '20251218_202313_images.jpeg', 'Kalpanax Krim 5 gram adalah salep antijamur topikal dengan kandungan utama Miconazole Nitrate 2% untuk mengobati infeksi kulit seperti kurap (tinea corporis, cruris, pedis/kutu air), panu (tinea versicolor), dan kandidiasis kulit, bekerja dengan membunuh jamur, dan tersedia di berbagai apotek daring dengan harga sekitar Rp15.000-Rp22.000. Oleskan 2-3 kali sehari pada area yang terinfeksi, lanjutkan 10 hari setelah gejala hilang agar tidak kambuh, dan hindari kontak dengan mata atau area mukosa.', 'Oleskan 2 kali sehari', 'Iritasi dan hipersensitivitas kulit', 'Miconazole nitrate 2%', 'Kalbe Farma', 'BPOM: DTL9711628129A1');

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

--
-- Dumping data untuk tabel `product_favorites`
--

INSERT INTO `product_favorites` (`id`, `user_id`, `product_id`, `created_at`) VALUES
(0, 4, 2, '2025-12-18 12:03:01'),
(0, 8, 0, '2025-12-23 14:08:57');

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

--
-- Dumping data untuk tabel `skin_data`
--

INSERT INTO `skin_data` (`id`, `user_id`, `skin_condition`, `severity`, `notes`, `created_at`) VALUES
(1, 2, 'berjerawat', 'moderate', 'Jerawat di area pipi dan dahi', '2025-12-09 12:57:33'),
(2, 2, 'berminyak', 'mild', 'Kulit berminyak di T-zone', '2025-12-09 12:57:33'),
(3, 3, 'normal', 'mild', 'Kondisi kulit normal', '2025-12-09 12:57:33'),
(4, 3, 'dermatitis_perioral', 'severe', 'Dermatitis di sekitar mulut', '2025-12-09 12:57:33');

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
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `is_admin`, `created_at`) VALUES
(1, 'Admin User', 'admin@example.com', 'pbkdf2:sha256:600000$...', 1, '2025-12-09 12:57:33'),
(2, 'John Doe', 'john@example.com', 'pbkdf2:sha256:600000$...', 0, '2025-12-09 12:57:33'),
(3, 'Jane Smith', 'jane@example.com', 'pbkdf2:sha256:600000$...', 0, '2025-12-09 12:57:33'),
(4, 'panji', 'panjirafi96@gmail.com', 'scrypt:32768:8:1$7HR1gzFvC1Skal90$6bffbd85f551dd7885b6720d3261c85b97c26238f37a1f130bbbf4c25cdbb4e6fa4c28bfaae05d12105d10fbf94ae8f2bafeeacea942f989ef6438009efb321f', 1, '2025-12-09 13:00:20'),
(5, 'Prasetyowati susiwi', 'prasetyowati@gmail.com', 'scrypt:32768:8:1$s8ttqcFkPl4LiGlD$709c37d67799bd0574c210ca48ff5017c12ea641f8fb5266cb1f5effdbb4c43786bb4db6db94d1e7450501cdbafd6453242fb186e62e001c125ba601ae04a047', 0, '2025-12-09 13:06:17'),
(7, 'Hah ?', 'frybanshee123@gmail.com', 'scrypt:32768:8:1$BbyjlvDj4ThkAEET$764d144d8b6c4288dec25538ddf934441eb7db3c9159aa18ca6d50329508c2259cffaa8a4c2e9f5690045b265879f3d32f5de8b12296104e48647ea0e976266b', 0, '2025-12-09 13:17:35'),
(8, 'Piresabil wistyorafa', 'fourducks12@gmail.com', 'scrypt:32768:8:1$ihKijexRtHY8CMnA$14fe9cc1b4a32a02c095c4557f82c640b25c0a7bb435c20254dc5c708d347c9cd73c25d1a0a1056ff7fea9a40aad808f34f9171713838f8ccb81936f559a0f49', 0, '2025-12-21 08:24:27');

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
-- Indeks untuk tabel `foods`
--
ALTER TABLE `foods`
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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT untuk tabel `daily_drink_logs`
--
ALTER TABLE `daily_drink_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `daily_food_logs`
--
ALTER TABLE `daily_food_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `daily_skin_analysis`
--
ALTER TABLE `daily_skin_analysis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `daily_sleep_logs`
--
ALTER TABLE `daily_sleep_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `drinks`
--
ALTER TABLE `drinks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `foods`
--
ALTER TABLE `foods`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `skin_data`
--
ALTER TABLE `skin_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

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
-- Ketidakleluasaan untuk tabel `skin_data`
--
ALTER TABLE `skin_data`
  ADD CONSTRAINT `skin_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
