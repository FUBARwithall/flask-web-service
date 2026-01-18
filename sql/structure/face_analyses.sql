CREATE TABLE face_analyses (
    id VARCHAR(36) PRIMARY KEY,
    user_id INT NOT NULL,
    timestamp VARCHAR(30),
    image_filename VARCHAR(255),
    image_url VARCHAR(255),
    skin_type VARCHAR(50),
    skin_type_confidence FLOAT,
    skin_type_predictions JSON,
    skin_problem VARCHAR(50),
    skin_problem_confidence FLOAT,
    skin_problem_predictions JSON,
    notes TEXT, //terbaru
    FOREIGN KEY (user_id) REFERENCES users(id)
);