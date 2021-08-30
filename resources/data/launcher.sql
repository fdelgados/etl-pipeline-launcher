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
    `aggregate_id` CHAR(36) NOT NULL,
    `event_name`   VARCHAR(100) NOT NULL,
    `event_data`   JSON         NOT NULL,
    `occurred_on`  DATETIME     NOT NULL,
    PRIMARY KEY `pk_event_store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX `event_store_event_name_index`
    ON event_store (`event_name`);

CREATE INDEX `event_store_aggregate_id_index`
    ON event_store (`aggregate_id`);

DROP TABLE IF EXISTS `pipelines`;
CREATE TABLE `pipelines`
(
    `id` BINARY(16) NOT NULL,
    `tenant_id` CHAR(36) NOT NULL,
    `launched_by` VARCHAR(30) NOT NULL,
    `completed` tinyint(1) DEFAULT 0 NOT NULL,
    PRIMARY KEY `pk_pipelines` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `pipelines_launcher_index`
    ON pipelines (`tenant_id`, `launched_by`);


