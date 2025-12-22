CREATE TABLE `daily_drink_logs` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `drink_id` int(11) NOT NULL,
    `quantity` int(11) NOT NULL,
    `log_date` date NOT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_drink_user` (`user_id`),
    KEY `fk_drink_drink` (`drink_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;