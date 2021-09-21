CREATE DATABASE IF NOT EXISTS duplicates CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE duplicates CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

GRANT INSERT, SELECT, UPDATE, DELETE ON duplicates.* TO 'duplicates';

FLUSH PRIVILEGES;

USE `duplicates`;

-- FUNCTIONS
DELIMITER //

CREATE FUNCTION UUID_TO_BIN(uuid CHAR(36))
    RETURNS BINARY(16) DETERMINISTIC
BEGIN
    RETURN UNHEX(CONCAT(REPLACE(uuid, '-', '')));
END; //

DELIMITER ;

DELIMITER //

CREATE FUNCTION BIN_TO_UUID(bin BINARY(16))
    RETURNS CHAR(36) DETERMINISTIC
BEGIN
    DECLARE hex CHAR(32);
    SET hex = HEX(bin);
    RETURN LOWER(CONCAT(LEFT(hex, 8), '-', MID(hex, 9, 4), '-', MID(hex, 13, 4), '-', MID(hex, 17, 4), '-', RIGHT(hex, 12)));
END; //

DELIMITER ;

-- TABLES

DROP TABLE IF EXISTS `reports`;
CREATE TABLE `reports`
(
    `id` BINARY(16) NOT NULL,
    `tenant_id` CHAR(36) NOT NULL,
    `name` VARCHAR(60) NOT NULL,
    `created_by` VARCHAR(30) NOT NULL,
    `completed` TINYINT(1) DEFAULT 0 NOT NULL,
    `k_shingle_size` TINYINT(1) NOT NULL,
    `similarity_threshold` DECIMAL(2, 1) NOT NULL,
    `started_on` DATETIME NOT NULL,
    `completed_on` DATETIME DEFAULT NULL,
    `total_pages` INT NOT NULL DEFAULT 0,
    `duplicated_pages` INT NOT NULL DEFAULT 0,
    `duplication_ratio` DECIMAL(5, 2) DEFAULT NULL,
    `duplication_average` DECIMAL(5, 2) DEFAULT NULL,
    `duplication_median` DECIMAL(5, 2) DEFAULT NULL,
    PRIMARY KEY `pk_reports` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `reports_creator_index`
    ON reports (`tenant_id`, `created_by`);

CREATE INDEX `reports_name_index`
    ON reports (`name`);

CREATE INDEX `reports_started_on_index`
    ON reports (`started_on`);
