CREATE DATABASE IF NOT EXISTS duplicates_emagister_it CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'emagister_it'@'%' IDENTIFIED BY '2bNWzc6guySaLCVV';

GRANT INSERT, SELECT, UPDATE, DELETE ON duplicates_emagister_it.* TO 'emagister_it';

FLUSH PRIVILEGES;

USE duplicates_emagister_it;

-- FUNCTIONS
DELIMITER //

CREATE FUNCTION IF NOT EXISTS UUID_TO_BIN(uuid CHAR(36))
    RETURNS BINARY(16) DETERMINISTIC
BEGIN
    RETURN UNHEX(CONCAT(REPLACE(uuid, '-', '')));
END; //

DELIMITER ;

DELIMITER //

CREATE FUNCTION IF NOT EXISTS BIN_TO_UUID(bin BINARY(16))
    RETURNS CHAR(36) DETERMINISTIC
BEGIN
    DECLARE hex CHAR(32);
    SET hex = HEX(bin);
    RETURN LOWER(CONCAT(LEFT(hex, 8), '-', MID(hex, 9, 4), '-', MID(hex, 13, 4), '-', MID(hex, 17, 4), '-', RIGHT(hex, 12)));
END; //

DELIMITER ;

-- TABLES

CREATE TABLE IF NOT EXISTS `reports`
(
    `id` BINARY(16) NOT NULL,
    `tenant_id` CHAR(36) NOT NULL,
    `name` VARCHAR(60) NOT NULL,
    `from_corpus` VARCHAR(25) NOT NULL,
    `created_by` VARCHAR(30) NOT NULL,
    `status` TINYINT(1) DEFAULT 0 NOT NULL,
    `k_shingle_size` TINYINT(1) NOT NULL,
    `similarity_threshold` DECIMAL(2, 1) NOT NULL,
    `similarity_threshold_margin` DECIMAL(3, 2) NOT NULL DEFAULT 0.0,
    `started_on` DATETIME NOT NULL,
    `completed_on` DATETIME DEFAULT NULL,
    `total_pages` INT NOT NULL DEFAULT 0,
    `duplicated_pages` INT NOT NULL DEFAULT 0,
    `duplication_ratio` DECIMAL(5, 2) DEFAULT NULL,
    `duplication_average` DECIMAL(5, 2) DEFAULT NULL,
    `duplication_median` DECIMAL(5, 2) DEFAULT NULL,
    PRIMARY KEY `pk_reports` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX IF NOT EXISTS `reports_creator_index`
    ON reports (`tenant_id`, `created_by`);

CREATE INDEX IF NOT EXISTS `reports_name_index`
    ON reports (`name`);

CREATE INDEX IF NOT EXISTS `reports_corpus_index`
    ON reports (`from_corpus`);

CREATE INDEX IF NOT EXISTS `reports_status_index`
    ON reports (`status`);

CREATE INDEX IF NOT EXISTS `reports_started_on_index`
    ON reports (`started_on`);


CREATE TABLE IF NOT EXISTS `duplicates`
(
    `report_id` BINARY(16) NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    `duplicate_url` VARCHAR(255) NOT NULL,
    `similarity` DECIMAL(8, 7) NOT NULL,
    `is_in_allowed_margin` TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY `pk_duplicates` (`report_id`, `url`, `duplicate_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX IF NOT EXISTS `duplicates_similarity`
    ON duplicates (`similarity`);

CREATE INDEX IF NOT EXISTS `duplicates_is_in_allowed_margin`
    ON duplicates (`is_in_allowed_margin`);

CREATE TABLE IF NOT EXISTS `event_store`
(
    `id`           CHAR(36),
    `aggregate_id` VARCHAR(255) NOT NULL,
    `event_name`   VARCHAR(200) NOT NULL,
    `event_data`   JSON         NOT NULL,
    `occurred_on`  DATETIME     NOT NULL,
    PRIMARY KEY `pk_event_store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX IF NOT EXISTS `event_store_event_name_index`
    ON event_store (`event_name`);

CREATE INDEX IF NOT EXISTS `event_store_aggregate_id_index`
    ON event_store (`aggregate_id`);

ALTER TABLE `event_store`
    ADD COLUMN IF NOT EXISTS `report_id` CHAR(36)
        GENERATED ALWAYS AS (
                JSON_UNQUOTE(JSON_EXTRACT(event_data, "$.report_id"))
            );
CREATE INDEX IF NOT EXISTS `event_store_event_data_index`
    ON event_store (`report_id`);
