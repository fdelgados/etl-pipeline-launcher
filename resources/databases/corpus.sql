CREATE DATABASE IF NOT EXISTS corpus CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'corpus'@'%' IDENTIFIED BY 'wTUbtEmk2S6R';

GRANT INSERT, SELECT, UPDATE, DELETE ON corpus.* TO 'corpus';

FLUSH PRIVILEGES;

USE `corpus`;

-- FUNCTIONS
DELIMITER //

CREATE FUNCTION IF NOT EXISTS UUID_TO_BIN(uuid CHAR(36))
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
CREATE TABLE IF NOT EXISTS `event_store`
(
    `id`           INT AUTO_INCREMENT,
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
ADD COLUMN IF NOT EXISTS `build_id` CHAR(36)
GENERATED ALWAYS AS (
    JSON_UNQUOTE(JSON_EXTRACT(event_data, "$.build_id"))
);
CREATE INDEX IF NOT EXISTS `event_store_event_data_index`
    ON event_store (`build_id`);

CREATE TABLE IF NOT EXISTS `builds`
(
    `id` BINARY(16) NOT NULL,
    `tenant_id` CHAR(36) NOT NULL,
    `name` VARCHAR(60) NOT NULL,
    `corpus_name` VARCHAR(25) NOT NULL,
    `total_requests` INT DEFAULT 0 NOT NULL,
    `successful_requests` INT DEFAULT 0 NOT NULL,
    `failed_requests` INT DEFAULT 0 NOT NULL,
    `started_by` VARCHAR(30) NOT NULL,
    `status` TINYINT(1) DEFAULT 0 NOT NULL,
    `started_on` DATETIME NOT NULL,
    `completed_on` DATETIME DEFAULT NULL,
    PRIMARY KEY `pk_builds` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX IF NOT EXISTS `builds_launcher_index`
    ON builds (`tenant_id`, `started_by`);

CREATE INDEX IF NOT EXISTS `builds_launcher_name_index`
    ON builds (`name`);

CREATE INDEX IF NOT EXISTS `builds_launcher_corpus_name_index`
    ON builds (`corpus_name`);


CREATE TABLE IF NOT EXISTS `corpora`
(
    `name` VARCHAR(25) NOT NULL,
    `tenant_id` CHAR(36) NOT NULL,
    `description` VARCHAR(120) DEFAULT NULL,
    `sitemaps` JSON NOT NULL,
    `request_headers` JSON DEFAULT NULL,
    `selector_mapping` JSON DEFAULT NULL,
    `excluded_tags` JSON DEFAULT NULL,
    `excluded_selectors` JSON DEFAULT NULL,
    `url_address_pattern` VARCHAR(150) DEFAULT NULL,
    `custom_request_fields` JSON DEFAULT NULL,
    PRIMARY KEY `pk_corpora` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
