CREATE TABLE `daily_sleep_logs` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `log_date` date NOT NULL,
    `sleep_hours` float NOT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_sleep_user` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;