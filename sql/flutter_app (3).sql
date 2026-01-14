-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Waktu pembuatan: 14 Jan 2026 pada 17.34
-- Versi server: 8.0.30
-- Versi PHP: 8.1.10

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
  `id` int NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `articles`
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
-- Struktur dari tabel `article_favorites`
--

CREATE TABLE `article_favorites` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `article_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `article_favorites`
--

INSERT INTO `article_favorites` (`id`, `user_id`, `article_id`, `created_at`) VALUES
(15, 5, 6, '2025-12-17 15:34:50'),
(17, 9, 4, '2026-01-14 07:46:51');

-- --------------------------------------------------------

--
-- Struktur dari tabel `daily_drink_logs`
--

CREATE TABLE `daily_drink_logs` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `drink_id` int NOT NULL,
  `quantity` int NOT NULL COMMENT 'gelas / botol',
  `log_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `daily_drink_logs`
--

INSERT INTO `daily_drink_logs` (`id`, `user_id`, `drink_id`, `quantity`, `log_date`) VALUES
(1, 1, 2, 5, '2025-12-22'),
(2, 1, 7, 1, '2025-12-22'),
(3, 1, 1, 1, '2025-12-24'),
(4, 5, 1, 1, '2026-01-02'),
(5, 7, 5, 1, '2026-01-05'),
(6, 9, 1, 1, '2026-01-14');

-- --------------------------------------------------------

--
-- Struktur dari tabel `daily_food_logs`
--

CREATE TABLE `daily_food_logs` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `food_id` int NOT NULL,
  `quantity` int NOT NULL COMMENT 'berapa kali/porsi',
  `log_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `daily_food_logs`
--

INSERT INTO `daily_food_logs` (`id`, `user_id`, `food_id`, `quantity`, `log_date`) VALUES
(1, 1, 3, 1, '2025-12-22'),
(2, 1, 2, 1, '2025-12-22'),
(3, 1, 1, 2, '2025-12-22'),
(4, 1, 3, 1, '2025-12-24'),
(5, 5, 2, 1, '2026-01-02'),
(6, 5, 1, 1, '2026-01-02'),
(7, 7, 1, 1, '2026-01-05'),
(8, 9, 2, 1, '2026-01-14');

-- --------------------------------------------------------

--
-- Struktur dari tabel `daily_skin_analysis`
--

CREATE TABLE `daily_skin_analysis` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `log_date` date NOT NULL,
  `total_oil` float NOT NULL,
  `total_simple_carb` float NOT NULL,
  `total_sugar` float NOT NULL,
  `total_fiber` float NOT NULL,
  `total_fermented` float NOT NULL,
  `hydration` float NOT NULL,
  `sleep_deficit` float NOT NULL,
  `skin_load_score` float NOT NULL,
  `status` enum('AMAN','WASPADA','OVER_LIMIT') COLLATE utf8mb4_general_ci NOT NULL,
  `main_triggers` text COLLATE utf8mb4_general_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `daily_skin_analysis`
--

INSERT INTO `daily_skin_analysis` (`id`, `user_id`, `log_date`, `total_oil`, `total_simple_carb`, `total_sugar`, `total_fiber`, `total_fermented`, `hydration`, `sleep_deficit`, `skin_load_score`, `status`, `main_triggers`, `created_at`) VALUES
(1, 1, '2025-12-22', 66, 42, 6, 12, 12, 54, 0, 88, 'OVER_LIMIT', 'Konsumsi minyak/gorengan berlebih; Konsumsi karbohidrat sederhana tinggi', '2025-12-22 04:45:29'),
(2, 3, '2025-12-24', 4, 1, 0, 0, 0, 1, 0.5, 5.25, 'WASPADA', 'Serat kurang; Hidrasi kurang', '2025-12-23 20:55:12'),
(3, 5, '2026-01-02', 5, 5, 1, 1, 1, 2, 1, 9.5, 'WASPADA', 'Serat kurang; Hidrasi kurang', '2026-01-01 21:01:11'),
(4, 7, '2026-01-05', 2, 1, 4, 1, 1, 0, 1, 6, 'WASPADA', 'Serat kurang; Hidrasi kurang', '2026-01-05 01:25:23'),
(5, 9, '2026-01-14', 3, 4, 1, 0, 0, 1, 1, 8.75, 'WASPADA', 'Serat kurang; Hidrasi kurang', '2026-01-14 07:52:40');

-- --------------------------------------------------------

--
-- Struktur dari tabel `daily_sleep_logs`
--

CREATE TABLE `daily_sleep_logs` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
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
(5, 1, '2025-12-24', 7.5),
(6, 5, '2026-01-02', 7),
(7, 7, '2026-01-05', 7),
(8, 9, '2026-01-14', 7);

-- --------------------------------------------------------

--
-- Struktur dari tabel `drinks`
--

CREATE TABLE `drinks` (
  `id` int NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `drink_type` enum('WATER','SWEET') COLLATE utf8mb4_general_ci NOT NULL,
  `sugar` tinyint DEFAULT '0' COMMENT '0–4 gula per unit'
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
-- Struktur dari tabel `face_analyses`
--

CREATE TABLE `face_analyses` (
  `id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL,
  `timestamp` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `image_filename` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `image_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `skin_type` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `skin_type_confidence` float DEFAULT NULL,
  `skin_type_predictions` json DEFAULT NULL,
  `skin_problem` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `skin_problem_confidence` float DEFAULT NULL,
  `skin_problem_predictions` json DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `face_analyses`
--

INSERT INTO `face_analyses` (`id`, `user_id`, `timestamp`, `image_filename`, `image_url`, `skin_type`, `skin_type_confidence`, `skin_type_predictions`, `skin_problem`, `skin_problem_confidence`, `skin_problem_predictions`) VALUES
('18edece6-187e-4a4b-8bd2-95ab2bf4529c', 9, '2026-01-14T08:36:46.529315Z', '18edece6-187e-4a4b-8bd2-95ab2bf4529c.jpg', '/static/uploads/analyses/18edece6-187e-4a4b-8bd2-95ab2bf4529c.jpg', 'Kering', 100, '{\"Kering\": 100.0, \"Normal\": 0.0, \"Berminyak\": 0.0}', 'Berjerawat', 100, '{\"Normal\": 0.0, \"Berjerawat\": 100.0, \"Dermatitis Perioral atau Ruam\": 0.0}'),
('62adf668-e4b6-441e-86b3-02c39091518f', 9, '2026-01-14T16:32:44.203474Z', '62adf668-e4b6-441e-86b3-02c39091518f.jpg', '/static/uploads/analyses/62adf668-e4b6-441e-86b3-02c39091518f.jpg', 'Kering', 100, '{\"Kering\": 100.0, \"Normal\": 0.0, \"Berminyak\": 0.0}', 'Berjerawat', 100, '{\"Normal\": 0.0, \"Berjerawat\": 100.0, \"Dermatitis Perioral atau Ruam\": 0.0}'),
('f9869f67-de1a-4ccd-abdb-b05a10205a53', 9, '2026-01-14T14:23:26.657585Z', 'f9869f67-de1a-4ccd-abdb-b05a10205a53.jpg', '/static/uploads/analyses/f9869f67-de1a-4ccd-abdb-b05a10205a53.jpg', 'Kering', 100, '{\"Kering\": 100.0, \"Normal\": 0.0, \"Berminyak\": 0.0}', 'Berjerawat', 100, '{\"Normal\": 0.0, \"Berjerawat\": 100.0, \"Dermatitis Perioral atau Ruam\": 0.0}');

-- --------------------------------------------------------

--
-- Struktur dari tabel `foods`
--

CREATE TABLE `foods` (
  `id` int NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `oil` tinyint NOT NULL COMMENT '0–4 minyak/gorengan',
  `simple_carb` tinyint NOT NULL COMMENT '0–4 karbo sederhana',
  `sugar` tinyint NOT NULL COMMENT '0–4 gula',
  `fiber` tinyint NOT NULL COMMENT '0–4 serat',
  `fermented` tinyint NOT NULL COMMENT '0–4 fermentasi'
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
-- Struktur dari tabel `glowmate`
--

CREATE TABLE `glowmate` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `type` enum('morning','afternoon','night') NOT NULL,
  `hour` int NOT NULL,
  `minute` int DEFAULT '0',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `glowmate`
--

INSERT INTO `glowmate` (`id`, `user_id`, `type`, `hour`, `minute`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 5, 'morning', 8, 47, 1, '2026-01-12 01:47:04', '2026-01-12 01:47:04'),
(2, 9, 'afternoon', 14, 53, 1, '2026-01-14 07:52:16', '2026-01-14 07:52:25');

-- --------------------------------------------------------

--
-- Struktur dari tabel `history_logs`
--

CREATE TABLE `history_logs` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `analysis_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `event_type` enum('VIEW_HISTORY','VIEW_DETAIL','DELETE','SHARE') NOT NULL,
  `metadata` json DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `products`
--

CREATE TABLE `products` (
  `id` int NOT NULL,
  `merek` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Brand name',
  `nama` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Product name',
  `harga` decimal(10,2) NOT NULL COMMENT 'Price',
  `kategori_penyakit` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Disease category',
  `image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Image path or URL',
  `deskripsi` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `dosis` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `efek_samping` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `komposisi` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `manufaktur` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nomor_registrasi` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Products table';

--
-- Dumping data untuk tabel `products`
--

INSERT INTO `products` (`id`, `merek`, `nama`, `harga`, `kategori_penyakit`, `image`, `deskripsi`, `dosis`, `efek_samping`, `komposisi`, `manufaktur`, `nomor_registrasi`) VALUES
(2, 'Azarine Hydrashoothe Sunscreen Gel', 'Azarine', 66900.00, 'Berjerawat', '20260113_212322_imagesazarinsunscreen.jpg', 'Tabir surya dalam bentuk gel untuk melembabkan dan melindungi kulit dari pengaruh buruk sinar matahari, sinar bluelight dan polusi. Di formulasikan dengan berbagai ukuran Hyaluronic Acid untuk melembabkan agar kulit kenyal. Kandungan vit C & E sebagai antioksidan. Tekstur gel ini dingin dan ringan, sehingga mudah', 'Oleskan pada wajah sebanyak dua jari sebelum menggunakan makeup', 'Efek samping bisa muncul jika Anda alergi bahan tertentu (periksa komposisi!), memiliki kulit iritasi berat, atau luka terbuka, yang bisa menyebabkan kemerahan atau gatal; hentikan pemakaian jika ada reaksi dan konsultasikan ke dokter', 'Water (Aqua): Pelarut dasar formula. Filter UV Kimiawi (Ethylhexyl Methoxycinnamate, Butyl Methoxydibenzoylmethane, Octocrylene): Melindungi kulit dari radiasi UVA dan UVB. Vitamin C (Ascorbic Acid): Antioksidan kuat, membantu mencerahkan dan menstimulasi kolagen. Ectoin: Melindungi dari blue light dan polusi, serta melembapkan. Hyaluronic Acid (11 Multikompleks): Melembapkan secara mendalam dan membuat kulit kenyal. Glycerin, Propanediol: Humektan untuk menjaga kelembapan kulit. Allantoin: Menenangkan kulit. Vitamin E (Tocopheryl Acetate): Antioksidan tambahan. Tekstur: Berbentuk krim-gel yang ringan, tidak lengket, dan cepat meresap tanpa meninggalkan residu putih (whitecast).', 'PT. Wahana Kosmetika Indonesia', 'NA 18211701919'),
(3, 'Hydrocortisone', 'Hydrocortison Cream 2.5% 5 g', 11400.00, 'Dermatitis Perioral', '20260113_215510_Hydrocortison_Cream.jpg', 'Informasi ini ditujukan bagi Tenaga Medis dan Kesehatan. Obat ini tergolong Obat Keras, sehingga penggunaan obat harus berdasarkan hasil konsultasi atau resep dokter. Hydrocortison Cream 2.5% 5 g adalah obat adrenokortikal steroid yang di gunakan untuk mengobati eksim, inflamasi, kemerahan,serta gatal-gatal pada kulit, beberapa jenis infeksi kulit yang dapat diobati contohnya dermatitis alergi, dermatitis kontak, dermatitis atopi, pruritus anogenital, neurodermatitis. Informasi Umum Terkait Kandungan: Cara kerjanya adalah dengan memiliki sifat anti-inflamasi (anti-peradangan), anti-pruritus (anti-gatal), dan vasokonstriktif (menyempitkan pembuluh darah), yang efektif meredakan gejala kemerahan, bengkak, dan gatal pada kulit.', 'PENGGUNAAN OBAT INI HARUS SESUAI DENGAN PETUNJUK DOKTER. Oleskan pada kulit yang bermasalah 1-2 kali per hari.', 'Pemakaian obat umumnya memiliki efek samping tertentu dan sesuai dengan masing-masing individu. Jika terjadi efek samping yang berlebih dan berbahaya, harap konsultasikan kepada tenaga medis. Efek samping yang mungkin terjadi dalam penggunaan obat adalah: Atrofi kulit, infeksi sekunder, rasa terbakar, iritasi, pruritus, hipopigmentasi, striae (garis-garis kulit), dan urtikaria.', 'Hydrocortisone acetate 2.5 %', 'Generic Manufacturer', 'BPOM RI: GKL7211642829B1');

-- --------------------------------------------------------

--
-- Struktur dari tabel `product_comments`
--

CREATE TABLE `product_comments` (
  `id` int NOT NULL,
  `product_id` int NOT NULL,
  `user_id` int NOT NULL,
  `comment` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `parent_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `product_comments`
--

INSERT INTO `product_comments` (`id`, `product_id`, `user_id`, `comment`, `created_at`, `parent_id`) VALUES
(3, 2, 5, 'cihuyyyy', '2026-01-13 14:25:06', NULL),
(5, 3, 8, 'okkk', '2026-01-13 15:38:22', NULL),
(6, 3, 5, 'asekk', '2026-01-13 15:45:59', 5),
(11, 3, 5, 'oyee', '2026-01-13 16:00:53', 6),
(12, 3, 5, 'sikattt', '2026-01-13 16:00:59', 11),
(14, 3, 5, 'soba abu', '2026-01-13 16:01:22', 12),
(17, 2, 8, 'keren', '2026-01-13 16:11:42', 3),
(18, 2, 8, 'mantap bang', '2026-01-13 16:11:53', 17),
(19, 3, 9, 'tes', '2026-01-14 07:44:01', 5);

-- --------------------------------------------------------

--
-- Struktur dari tabel `product_favorites`
--

CREATE TABLE `product_favorites` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `product_favorites`
--

INSERT INTO `product_favorites` (`id`, `user_id`, `product_id`, `created_at`) VALUES
(7, 9, 2, '2026-01-14 07:47:01');

-- --------------------------------------------------------

--
-- Stand-in struktur untuk tampilan `skin_condition_summary`
-- (Lihat di bawah untuk tampilan aktual)
--
CREATE TABLE `skin_condition_summary` (
`skin_condition` varchar(255)
,`count` bigint
,`percentage` decimal(26,2)
);

-- --------------------------------------------------------

--
-- Struktur dari tabel `skin_data`
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
-- Dumping data untuk tabel `skin_data`
--

INSERT INTO `skin_data` (`id`, `user_id`, `skin_condition`, `severity`, `notes`, `created_at`) VALUES
(1, 2, 'berjerawat', 'moderate', 'Jerawat di area pipi dan dahi', '2025-12-10 03:47:57'),
(2, 2, 'berminyak', 'mild', 'Kulit berminyak di T-zone', '2025-12-10 03:47:57'),
(3, 3, 'normal', 'mild', 'Kondisi kulit normal', '2025-12-10 03:47:57'),
(4, 3, 'dermatitis_perioral', 'severe', 'Dermatitis di sekitar mulut', '2025-12-10 03:47:57');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
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
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `is_admin`, `created_at`) VALUES
(1, 'Admin User', 'admin@example.com', 'pbkdf2:sha256:600000$...', 1, '2025-12-10 03:47:57'),
(2, 'John Doe', 'john@example.com', 'pbkdf2:sha256:600000$...', 0, '2025-12-10 03:47:57'),
(3, 'Jane Smith', 'jane@example.com', 'pbkdf2:sha256:600000$...', 0, '2025-12-10 03:47:57'),
(4, 'bintang', 'bintang@gmail.com', 'scrypt:32768:8:1$9lSWe1uhdf8N4SLK$e988c75c7eda1dda57e6e8aefadde266cb110ac37752c5d7da9b7ce2e9829595d527a06d000f9da3106b09c2a8af006796b1f0d46729643a38b36a4c91f58d84', 1, '2025-12-10 03:48:59'),
(5, 'Bintang Rafli Priatama', 'bintangrafli73@gmail.com', 'scrypt:32768:8:1$a3C3Sap3q5EkDtU0$12bf40d681e521505f7cb3d3fff9c94048a4c5c9f281dd67612419f0d07304bd4efa2c0c9329ce375ea50c62512bd0a3911a9aa6a49bd8da257cd6715faba7bd', 0, '2025-12-10 03:51:12'),
(7, 'Panji', 'frybanshee123@gmail.com', 'scrypt:32768:8:1$YrAs2hl9JWYBvk2w$73f12fa45307fb130b1101007bd159cc2ce133ad8d1abc37fd903955c7b0bc08c7ab3259bbda0974590d21cd1aff56ebf74ba0ab1c5789bbb471361f5059c0de', 0, '2026-01-05 01:22:35'),
(8, 'Rafli Haryanto', 'bintangrafli76@gmail.com', 'scrypt:32768:8:1$JpBBGOq5CtDM2UEi$777d9b623603c3aeca9c1ed33ab497a99ec2e59c4869d50de9d05a515decda4d7116455e3ab51cf063faae7ac42f064bfe183c0358ce9d073f286786218e126e', 0, '2026-01-13 15:23:47'),
(9, 'Stevan Sasono', 'catt147ok@gmail.com', 'scrypt:32768:8:1$UyRoSPVcntbQ3H38$4adff6acc9531a5e1b72e6eaaeae84d440a188378ea11ee2633529f6236ea0fd3dfb054c8e818cbf0c9a1d9235b45d8c117258e3b7dfcccc46077da5ce6c09a4', 0, '2026-01-14 07:43:39');

-- --------------------------------------------------------

--
-- Stand-in struktur untuk tampilan `user_latest_record`
-- (Lihat di bawah untuk tampilan aktual)
--
CREATE TABLE `user_latest_record` (
`id` int
,`name` varchar(255)
,`email` varchar(255)
,`user_created_at` timestamp
,`skin_condition` varchar(255)
,`severity` varchar(100)
,`record_created_at` timestamp
,`record_rank` bigint unsigned
);

-- --------------------------------------------------------

--
-- Stand-in struktur untuk tampilan `user_statistics`
-- (Lihat di bawah untuk tampilan aktual)
--
CREATE TABLE `user_statistics` (
`total_users` bigint
,`total_regular_users` bigint
,`total_admins` bigint
,`total_skin_records` bigint
);

-- --------------------------------------------------------

--
-- Struktur untuk view `skin_condition_summary`
--
DROP TABLE IF EXISTS `skin_condition_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `skin_condition_summary`  AS SELECT `skin_data`.`skin_condition` AS `skin_condition`, count(0) AS `count`, round(((count(0) * 100.0) / (select count(0) from `skin_data`)),2) AS `percentage` FROM `skin_data` WHERE (`skin_data`.`skin_condition` is not null) GROUP BY `skin_data`.`skin_condition` ORDER BY `count` DESC ;

-- --------------------------------------------------------

--
-- Struktur untuk view `user_latest_record`
--
DROP TABLE IF EXISTS `user_latest_record`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `user_latest_record`  AS SELECT `u`.`id` AS `id`, `u`.`name` AS `name`, `u`.`email` AS `email`, `u`.`created_at` AS `user_created_at`, `sd`.`skin_condition` AS `skin_condition`, `sd`.`severity` AS `severity`, `sd`.`created_at` AS `record_created_at`, row_number() OVER (PARTITION BY `u`.`id` ORDER BY `sd`.`created_at` desc ) AS `record_rank` FROM (`users` `u` left join `skin_data` `sd` on((`u`.`id` = `sd`.`user_id`))) ;

-- --------------------------------------------------------

--
-- Struktur untuk view `user_statistics`
--
DROP TABLE IF EXISTS `user_statistics`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `user_statistics`  AS SELECT count(distinct `u`.`id`) AS `total_users`, count(distinct (case when (`u`.`is_admin` = 0) then `u`.`id` end)) AS `total_regular_users`, count(distinct (case when (`u`.`is_admin` = 1) then `u`.`id` end)) AS `total_admins`, count(distinct `sd`.`id`) AS `total_skin_records` FROM (`users` `u` left join `skin_data` `sd` on((`u`.`id` = `sd`.`user_id`))) ;

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
-- Indeks untuk tabel `article_favorites`
--
ALTER TABLE `article_favorites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_article` (`user_id`,`article_id`),
  ADD KEY `article_id` (`article_id`);

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
  ADD KEY `fk_face_user` (`user_id`);

--
-- Indeks untuk tabel `foods`
--
ALTER TABLE `foods`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `glowmate`
--
ALTER TABLE `glowmate`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `history_logs`
--
ALTER TABLE `history_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_event` (`user_id`,`event_type`),
  ADD KEY `idx_analysis` (`analysis_id`),
  ADD KEY `idx_created` (`created_at`);

--
-- Indeks untuk tabel `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_merek` (`merek`),
  ADD KEY `idx_kategori_penyakit` (`kategori_penyakit`);

--
-- Indeks untuk tabel `product_comments`
--
ALTER TABLE `product_comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `parent_id` (`parent_id`);

--
-- Indeks untuk tabel `product_favorites`
--
ALTER TABLE `product_favorites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_product` (`user_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

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
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT untuk tabel `article_favorites`
--
ALTER TABLE `article_favorites`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT untuk tabel `daily_drink_logs`
--
ALTER TABLE `daily_drink_logs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT untuk tabel `daily_food_logs`
--
ALTER TABLE `daily_food_logs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `daily_skin_analysis`
--
ALTER TABLE `daily_skin_analysis`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `daily_sleep_logs`
--
ALTER TABLE `daily_sleep_logs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `glowmate`
--
ALTER TABLE `glowmate`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `history_logs`
--
ALTER TABLE `history_logs`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `products`
--
ALTER TABLE `products`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `product_comments`
--
ALTER TABLE `product_comments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT untuk tabel `product_favorites`
--
ALTER TABLE `product_favorites`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT untuk tabel `skin_data`
--
ALTER TABLE `skin_data`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `article_favorites`
--
ALTER TABLE `article_favorites`
  ADD CONSTRAINT `article_favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `article_favorites_ibfk_2` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `glowmate`
--
ALTER TABLE `glowmate`
  ADD CONSTRAINT `glowmate_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ketidakleluasaan untuk tabel `history_logs`
--
ALTER TABLE `history_logs`
  ADD CONSTRAINT `fk_history_analysis` FOREIGN KEY (`analysis_id`) REFERENCES `face_analyses` (`id`) ON DELETE SET NULL;

--
-- Ketidakleluasaan untuk tabel `product_comments`
--
ALTER TABLE `product_comments`
  ADD CONSTRAINT `product_comments_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_comments_ibfk_3` FOREIGN KEY (`parent_id`) REFERENCES `product_comments` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `product_favorites`
--
ALTER TABLE `product_favorites`
  ADD CONSTRAINT `product_favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_favorites_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `skin_data`
--
ALTER TABLE `skin_data`
  ADD CONSTRAINT `skin_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
