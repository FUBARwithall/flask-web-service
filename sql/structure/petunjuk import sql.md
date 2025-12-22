# Instruksi Import Database

Ikuti langkah-langkah berikut untuk mengimpor struktur database dengan aman dan tanpa error. Import dilakukan secara bertahap agar tidak terjadi konflik dependensi atau foreign key.

## Import Struktur Tabel
Import setiap tabel menggunakan perintah `CREATE TABLE` secara terpisah dan **jangan mengimpor data (`INSERT`) pada tahap ini**. Urutan import yang disarankan adalah: `users`, `articles`, `drinks`, `foods`, `products`, `article_favorites`, `product_favorites`, `daily_drink_logs`, `daily_food_logs`, `daily_sleep_logs`, `daily_skin_analysis`, dan `skin_data`. Pastikan setiap tabel berhasil dibuat sebelum melanjutkan ke tabel berikutnya.

## Cek Struktur
Setelah semua tabel selesai diimpor, pastikan seluruh tabel sudah tersedia, engine tabel menggunakan **InnoDB**, setiap tabel memiliki **PRIMARY KEY**, dan tidak ada error selama proses import.

## Import Foreign Key
Setelah semua tabel tersedia dan tervalidasi, jalankan file `foreign_keys.sql` yang berisi perintah `ALTER TABLE` untuk menambahkan seluruh foreign key constraint. Jangan menjalankan foreign key sebelum semua tabel dibuat.

## Import Data (Opsional)
Jika struktur tabel dan foreign key sudah berhasil diterapkan, data dapat diimpor menggunakan perintah `INSERT`. Disarankan import data dilakukan setelah foreign key aktif agar integritas data tetap terjaga.

## Catatan Penting
Jika muncul error `Cannot add foreign key constraint`, pastikan tipe data kolom foreign key dan primary key sama persis, tidak ada data lama dengan relasi rusak, serta charset dan collation antar tabel konsisten. Untuk troubleshooting lanjutan, gunakan perintah `SHOW ENGINE INNODB STATUS;`.

Dokumen ini dibuat untuk memastikan proses setup database berjalan stabil, terstruktur, dan bebas konflik relasi.