CREATE TABLE `glowmate` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `type` enum('morning','afternoon','night') NOT NULL,
  `hour` int NOT NULL,
  `minute` int DEFAULT '0',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;