-- Create Airflow database (for Airflow metadata)
CREATE DATABASE IF NOT EXISTS airflow
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Create Playstore database (for app data)
CREATE DATABASE IF NOT EXISTS playstore
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE playstore;

CREATE TABLE IF NOT EXISTS play_store_apps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app VARCHAR(255),
    category VARCHAR(100),
    rating DECIMAL(3,1),
    reviews INT,
    size VARCHAR(20),
    installs VARCHAR(50),
    `type` VARCHAR(20),
    price VARCHAR(20),
    content_rating VARCHAR(50),
    genres VARCHAR(255),
    last_updated DATE,
    current_ver VARCHAR(50),
    android_ver VARCHAR(50)
);
