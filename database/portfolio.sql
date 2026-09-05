-- Portfolio Database Schema (MySQL Compatible)
-- Designed for Kathiresan - Computer Science and Engineering Student Portfolio

CREATE DATABASE IF NOT EXISTS portfolio_db;
USE portfolio_db;

-- Messages Table
-- Stores contact form submissions from website visitors
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
