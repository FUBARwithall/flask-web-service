CREATE TABLE `article_favorites` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `article_id` int(11) NOT NULL,
    `created_at` timestamp NULL DEFAULT current_timestamp (),
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;