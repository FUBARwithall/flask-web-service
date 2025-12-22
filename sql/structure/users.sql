CREATE TABLE `users` (
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