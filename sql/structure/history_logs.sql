
CREATE TABLE `history_logs` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `analysis_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `event_type` enum('VIEW_HISTORY','VIEW_DETAIL','DELETE','SHARE') NOT NULL,
  `metadata` json DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Indeks untuk tabel `history_logs`
--
ALTER TABLE `history_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_event` (`user_id`,`event_type`),
  ADD KEY `idx_analysis` (`analysis_id`),
  ADD KEY `idx_created` (`created_at`);
