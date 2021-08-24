CREATE USER 'launcher'@'%' IDENTIFIED BY 'wTUbtEmk2S6R';

CREATE DATABASE launcher CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

GRANT INSERT, SELECT, UPDATE, DELETE ON launcher.* TO 'launcher';

FLUSH PRIVILEGES;

USE `launcher`;

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


DELIMITER //
CREATE DEFINER=`launcher`@`localhost` FUNCTION `ordered_uuid`(uuid BINARY(36))
    RETURNS binary(16) DETERMINISTIC
    RETURN UNHEX(CONCAT(SUBSTR(uuid, 15, 4),SUBSTR(uuid, 10, 4),SUBSTR(uuid, 1, 8),SUBSTR(uuid, 20, 4),SUBSTR(uuid, 25)));
//
DELIMITER ;

