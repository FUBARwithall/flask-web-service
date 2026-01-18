CREATE TABLE body_analyses (
    id VARCHAR(36) PRIMARY KEY,
    user_id INT NOT NULL,
    timestamp VARCHAR(30),
    image_filename VARCHAR(255),
    image_url VARCHAR(255),
    disease_key VARCHAR(50),
    disease_name VARCHAR(100),
    confidence FLOAT,
    all_predictions JSON,
    notes TEXT, //terbaru
    FOREIGN KEY (user_id) REFERENCES users(id)
);
