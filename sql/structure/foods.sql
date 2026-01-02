CREATE TABLE `foods` (
    `id` int(11) NOT NULL,
    `name` varchar(100) NOT NULL,
    `oil` tinyint (4) NOT NULL COMMENT '0–4 minyak/gorengan',
    `simple_carb` tinyint (4) NOT NULL COMMENT '0–4 karbo sederhana',
    `sugar` tinyint (4) NOT NULL COMMENT '0–4 gula',
    `fiber` tinyint (4) NOT NULL COMMENT '0–4 serat',
    `fermented` tinyint (4) NOT NULL COMMENT '0–4 fermentasi'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;