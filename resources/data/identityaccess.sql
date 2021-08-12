CREATE USER 'master'@'%' IDENTIFIED BY 'hY54t68WGWpd';

CREATE DATABASE identity_access CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

GRANT INSERT, SELECT, UPDATE, DELETE ON identity_access.* TO 'master'@'%';

FLUSH PRIVILEGES;

USE `identity_access`;

DROP TABLE IF EXISTS `tenants`;
CREATE TABLE `tenants`
(
    `id` BINARY(16) NOT NULL,
    `company_name` VARCHAR(100) NOT NULL,
    `active` tinyint(1) DEFAULT 0 NOT NULL,
    PRIMARY KEY `pk_tenants` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`
(
    `username` VARCHAR(30) NOT NULL,
    `tenant_id` BINARY(16) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `password` CHAR(40) NOT NULL,
    `first_name` VARCHAR(50) NULL,
    `last_name` VARCHAR(100) NULL,
    `role` VARCHAR(30) NOT NULL,
    `is_enabled` tinyint(1) DEFAULT 0 NOT NULL,
    PRIMARY KEY `pk_users` (`username`, `tenant_id`),
    CONSTRAINT `fk_users_tenants` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `users_tenant_id_index`
    ON users (`password`);


DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles`
(
    `name` VARCHAR(30) NOT NULL,
    `description` VARCHAR(100) NULL DEFAULT NULL,
    PRIMARY KEY `pk_roles` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `scopes`;
CREATE TABLE `scopes`
(
    `name` VARCHAR(30) NOT NULL,
    `description` VARCHAR(100) NULL DEFAULT NULL,
    PRIMARY KEY `pk_scopes` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions`
(
    `tenant_id` BINARY(16) NOT NULL,
    `role_name` VARCHAR(30) NOT NULL,
    `scope_name` VARCHAR(30) NOT NULL,
    PRIMARY KEY `pk_permissions` (`tenant_id`, `role_name`, `scope_name`),
    CONSTRAINT `fk_permissions_tenants` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_permissions_roles` FOREIGN KEY (`role_name`) REFERENCES `roles`(`name`) ON DELETE CASCADE,
    CONSTRAINT `fk_permissions_scopes` FOREIGN KEY (`scope_name`) REFERENCES `scopes`(`name`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `ordered_uuid`(uuid BINARY(36))
    RETURNS binary(16) DETERMINISTIC
    RETURN UNHEX(CONCAT(SUBSTR(uuid, 15, 4),SUBSTR(uuid, 10, 4),SUBSTR(uuid, 1, 8),SUBSTR(uuid, 20, 4),SUBSTR(uuid, 25)));
//
DELIMITER ;

INSERT INTO tenants(id, company_name, active) VALUES (ordered_uuid('ba8f5129-2839-4658-b66e-9d2a04947cad'), 'Emagister', 1);
