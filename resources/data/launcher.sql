CREATE USER 'launcher'@'%' IDENTIFIED BY 'wTUbtEmk2S6R';

CREATE DATABASE launcher CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

GRANT INSERT, SELECT, UPDATE, DELETE ON launcher.* TO 'launcher';

FLUSH PRIVILEGES;

USE `launcher`;

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

DROP TABLE IF EXISTS `event_store`;
CREATE TABLE `event_store`
(
    `id`           INT AUTO_INCREMENT,
    `pipeline_id` CHAR(36) NOT NULL,
    `aggregate_id` VARCHAR(255) NOT NULL,
    `event_name`   VARCHAR(100) NOT NULL,
    `event_data`   JSON         NOT NULL,
    `occurred_on`  DATETIME     NOT NULL,
    PRIMARY KEY `pk_event_store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX `event_store_event_name_index`
    ON event_store (`event_name`);

CREATE INDEX `event_store_aggregate_id_index`
    ON event_store (`aggregate_id`);

CREATE INDEX `event_store_pipeline_id_index`
    ON event_store (`pipeline_id`);

DROP TABLE IF EXISTS `pipelines`;
CREATE TABLE `pipelines`
(
    `id` BINARY(16) NOT NULL,
    `tenant_id` CHAR(36) NOT NULL,
    `name` VARCHAR(60) NOT NULL,
    `description` VARCHAR(200) DEFAULT NULL,
    `launched_by` VARCHAR(30) NOT NULL,
    `completed` TINYINT(1) DEFAULT 0 NOT NULL,
    `request_headers` JSON DEFAULT NULL,
    `selector_mapping` JSON DEFAULT NULL,
    `excluded_tags` JSON DEFAULT NULL,
    `excluded_selectors` JSON DEFAULT NULL,
    `sitemaps_urls` JSON NOT NULL,
    `url_address_pattern` VARCHAR(255) DEFAULT NULL,
    `started_on` DATETIME NOT NULL,
    `completed_on` DATETIME DEFAULT NULL,
    `custom_request_fields` JSON DEFAULT NULL,
    PRIMARY KEY `pk_pipelines` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `pipelines_launcher_index`
    ON pipelines (`tenant_id`, `launched_by`);

CREATE INDEX `pipelines_launcher_name_index`
    ON pipelines (`name`);

CREATE INDEX `pipelines_launcher_started_on_index`
    ON pipelines (`started_on`);

DROP TABLE IF EXISTS `web_corpus`;
CREATE TABLE `web_corpus`
(
    `address`           VARCHAR(255) NOT NULL,
    `status_code`       INT          NOT NULL,
    `status`            VARCHAR(50)  NOT NULL,
    `h1`                VARCHAR(255) NULL,
    `title`             VARCHAR(255) NULL,
    `content`           MEDIUMTEXT   NULL,
    `is_indexable`      TINYINT(1)   NULL,
    `final_address`     VARCHAR(255) NULL,
    `canonical_address` VARCHAR(255) NULL,
    `datalayer`         MEDIUMTEXT  NULL,
    `modified_on` DATETIME     NOT NULL,
    PRIMARY KEY `pk_web_corpus` (`address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX `web_corpus_status_code_index`
    ON web_corpus (`status_code`);

CREATE INDEX `web_corpus_final_address_index`
    ON web_corpus (`final_address`);

CREATE INDEX `web_corpus_canonical_address_index`
    ON web_corpus (`canonical_address`);

