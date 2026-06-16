CREATE DATABASE IF NOT EXISTS todo_db;

USE todo_db;

CREATE TABLE IF NOT EXISTS todos (
    id INT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    priority INT NOT NULL,
    description TEXT NULL
);
