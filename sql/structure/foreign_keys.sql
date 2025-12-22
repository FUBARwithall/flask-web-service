ALTER TABLE `daily_drink_logs`
ADD CONSTRAINT `fk_drink_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
ADD CONSTRAINT `fk_drink_drink` FOREIGN KEY (`drink_id`) REFERENCES `drinks` (`id`);

ALTER TABLE `daily_food_logs`
ADD CONSTRAINT `fk_food_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
ADD CONSTRAINT `fk_food_food` FOREIGN KEY (`food_id`) REFERENCES `foods` (`id`);

ALTER TABLE `daily_sleep_logs`
ADD CONSTRAINT `fk_sleep_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `daily_skin_analysis`
ADD CONSTRAINT `fk_analysis_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `skin_data`
ADD CONSTRAINT `skin_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;