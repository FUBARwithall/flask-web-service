CREATE TABLE `products` (
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

-- update tipe data efek_samping
ALTER TABLE products
MODIFY efek_samping VARCHAR(500)
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci
NULL;
