CREATE TABLE `daily_food_logs` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `food_id` int(11) NOT NULL,
    `quantity` int(11) NOT NULL,
    `log_date` date NOT NULL,
    PRIMARY KEY (`id`),
    KEY `fk_food_user` (`user_id`),
    KEY `fk_food_food` (`food_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;