CREATE DATABASE IF NOT EXISTS poultry;
CREATE USER IF NOT EXISTS 'poultry'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON poultry.* TO 'poultry'@'localhost';
FLUSH PRIVILEGES;