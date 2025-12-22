SELECT
    COALESCE(SUM(f.oil * fl.quantity), 0) AS total_oil,
    COALESCE(
        SUM(f.simple_carb * fl.quantity),
        0
    ) AS total_simple_carb,
    COALESCE(SUM(f.sugar * fl.quantity), 0) AS food_sugar,
    COALESCE(SUM(f.fiber * fl.quantity), 0) AS total_fiber,
    COALESCE(
        SUM(f.fermented * fl.quantity),
        0
    ) AS total_fermented,
    COALESCE(
        SUM(
            CASE
                WHEN dl.drink_type = 'WATER' THEN dl.quantity
                ELSE 0
            END
        ),
        0
    ) AS hydration,
    COALESCE(
        SUM(
            CASE
                WHEN dl.drink_type = 'SWEET' THEN dl.sugar * dl.quantity
                ELSE 0
            END
        ),
        0
    ) AS liquid_sugar,
    COALESCE(sl.sleep_hours, 0) AS sleep_hours
FROM
    users u
    LEFT JOIN daily_food_logs fl ON u.id = fl.user_id
    AND fl.log_date = '2025-01-10'
    LEFT JOIN foods f ON fl.food_id = f.id
    LEFT JOIN daily_drink_logs dl ON u.id = dl.user_id
    AND dl.log_date = '2025-01-10'
    LEFT JOIN daily_sleep_logs sl ON u.id = sl.user_id
    AND sl.log_date = '2025-01-10'
WHERE
    u.id = 1
GROUP BY
    sl.sleep_hours;