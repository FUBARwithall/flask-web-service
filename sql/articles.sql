-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 10 Des 2025 pada 02.44
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
  `image` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
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
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
