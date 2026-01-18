-- Add note column to face_analyses table
ALTER TABLE face_analyses 
ADD COLUMN note TEXT NULL AFTER skin_problem_predictions;

-- Add note column to body_analyses table
ALTER TABLE body_analyses 
ADD COLUMN note TEXT NULL AFTER all_predictions;
