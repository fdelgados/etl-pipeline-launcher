CREATE DATABASE IF NOT EXISTS corpus_emagister_it CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


DELIMITER //

CREATE FUNCTION UUID_TO_BIN(uuid CHAR(36)) RETURNS BINARY(16) DETERMINISTIC
BEGIN
    RETURN UNHEX(CONCAT(REPLACE(uuid, '-', '')));
END;
//
CREATE FUNCTION BIN_TO_UUID(bin BINARY(16)) RETURNS CHAR(36) DETERMINISTIC
BEGIN
    DECLARE hex CHAR(32);
    SET hex = HEX(bin);
    RETURN LOWER(CONCAT(LEFT(hex, 8), '-', MID(hex, 9, 4), '-', MID(hex, 13, 4), '-', MID(hex, 17, 4), '-', RIGHT(hex, 12)));
END;

//
DELIMITER ;

CREATE USER IF NOT EXISTS 'emagister_it'@'%' IDENTIFIED BY '2bNWzc6guySaLCVV';

GRANT INSERT, SELECT, UPDATE, DELETE ON corpus_emagister_it.* TO 'emagister_it';
GRANT EXECUTE ON FUNCTION corpus_emagister_com.UUID_TO_BIN TO 'emagister_it';
GRANT EXECUTE ON FUNCTION corpus_emagister_com.BIN_TO_UUID TO 'emagister_it';

FLUSH PRIVILEGES;

USE corpus_emagister_it;

-- TABLES
CREATE TABLE IF NOT EXISTS `event_store`
(
    `id`           CHAR(36),
    `aggregate_id` VARCHAR(255) NOT NULL,
    `event_name`   VARCHAR(200) NOT NULL,
    `event_data`   JSON         NOT NULL,
    `occurred_on`  DATETIME(6)     NOT NULL,
    PRIMARY KEY `pk_event_store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX IF NOT EXISTS `event_store_event_name_index`
    ON event_store (`event_name`);

CREATE INDEX IF NOT EXISTS `event_store_aggregate_id_index`
    ON event_store (`aggregate_id`);

CREATE INDEX IF NOT EXISTS `event_store_event_data_index`
    ON event_store (`event_data`);

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
