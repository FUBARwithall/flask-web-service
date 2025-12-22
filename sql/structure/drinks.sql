CREATE TABLE `drinks` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `drink_type` enum ('WATER', 'SWEET') NOT NULL,
    `sugar` tinyint (4) DEFAULT 0,
    PRIMARY KEY (`id`),
    KEY `idx_drink_type` (`drink_type`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;