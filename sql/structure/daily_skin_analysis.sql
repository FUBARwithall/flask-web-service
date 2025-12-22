CREATE TABLE `daily_skin_analysis` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `log_date` date NOT NULL,
    `total_oil` float NOT NULL,
    `total_simple_carb` float NOT NULL,
    `total_sugar` float NOT NULL,
    `total_fiber` float NOT NULL,
    `total_fermented` float NOT NULL,
    `hydration` float NOT NULL,
    `sleep_deficit` float NOT NULL,
    `skin_load_score` float NOT NULL,
    `status` enum (
        'AMAN',
        'WASPADA',
        'OVER_LIMIT'
    ) NOT NULL,
    `main_triggers` text DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp (),
    PRIMARY KEY (`id`),
    KEY `fk_analysis_user` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;