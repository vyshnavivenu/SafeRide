-- =========================================================
-- SAFERIDE: DRIVER VERIFICATION & PASSENGER SAFETY SYSTEM
-- DATABASE TABLE DEFINITIONS (XAMPP MySQL / MariaDB)
-- Matches System Form Design & Table Design Specification
-- =========================================================

CREATE DATABASE IF NOT EXISTS `saferide_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `saferide_db`;

-- ---------------------------------------------------------
-- Table 1: tbl_passenger
-- Description: Stores passenger user profile and login info
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS `tbl_passenger` (
    `passenger_id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `phone_number` VARCHAR(15) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `emergency_contact_1_name` VARCHAR(100) DEFAULT NULL,
    `emergency_contact_1_phone` VARCHAR(20) DEFAULT NULL,
    `emergency_contact_1_relation` VARCHAR(50) DEFAULT 'Family',
    `emergency_contact_2_name` VARCHAR(100) DEFAULT NULL,
    `emergency_contact_2_phone` VARCHAR(20) DEFAULT NULL,
    `emergency_contact_2_relation` VARCHAR(50) DEFAULT 'Friend',
    `emergency_contact_3_name` VARCHAR(100) DEFAULT NULL,
    `emergency_contact_3_phone` VARCHAR(20) DEFAULT NULL,
    `emergency_contact_3_relation` VARCHAR(50) DEFAULT 'Guardian',
    `address` TEXT DEFAULT NULL,
    `profile_photo` VARCHAR(255) DEFAULT NULL,
    `user_id` BIGINT(20) DEFAULT NULL,
    PRIMARY KEY (`passenger_id`),
    UNIQUE KEY `uk_passenger_email` (`email`),
    UNIQUE KEY `uk_passenger_phone` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table 2: tbl_driver
-- Description: Stores registered driver & vehicle attributes
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS `tbl_driver` (
    `driver_id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `phone_number` VARCHAR(15) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `license_number` VARCHAR(30) NOT NULL,
    `vehicle_number` VARCHAR(20) NOT NULL,
    `vehicle_type` VARCHAR(20) NOT NULL DEFAULT 'auto',
    `verification_status` VARCHAR(15) NOT NULL DEFAULT 'Pending',
    `qr_code` VARCHAR(255) DEFAULT NULL,
    `password` VARCHAR(255) NOT NULL,
    `experience_years` INT(10) UNSIGNED NOT NULL DEFAULT 1,
    `verification_notes` TEXT DEFAULT NULL,
    `verified_at` DATETIME DEFAULT NULL,
    `verification_token` CHAR(36) NOT NULL,
    `reputation_score` DOUBLE NOT NULL DEFAULT 85.0,
    `total_trips` INT(10) UNSIGNED NOT NULL DEFAULT 0,
    `average_rating` DOUBLE NOT NULL DEFAULT 5.0,
    `driver_photo` VARCHAR(255) DEFAULT NULL,
    `license_doc` VARCHAR(255) DEFAULT NULL,
    `id_proof_doc` VARCHAR(255) DEFAULT NULL,
    `police_clearance_doc` VARCHAR(255) DEFAULT NULL,
    `qr_code_image` VARCHAR(255) DEFAULT NULL,
    `user_id` BIGINT(20) DEFAULT NULL,
    PRIMARY KEY (`driver_id`),
    UNIQUE KEY `uk_driver_phone` (`phone_number`),
    UNIQUE KEY `uk_driver_email` (`email`),
    UNIQUE KEY `uk_driver_license` (`license_number`),
    UNIQUE KEY `uk_driver_vehicle` (`vehicle_number`),
    UNIQUE KEY `uk_driver_token` (`verification_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table 3: tbl_admin
-- Description: Stores administrator credentials
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS `tbl_admin` (
    `admin_id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `user_id` BIGINT(20) DEFAULT NULL,
    PRIMARY KEY (`admin_id`),
    UNIQUE KEY `uk_admin_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table 4: tbl_vehicle_documents
-- Description: Stores uploaded KYC licence and RC documents
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS `tbl_vehicle_documents` (
    `document_id` INT(11) NOT NULL AUTO_INCREMENT,
    `driver_id` INT(11) NOT NULL,
    `license_doc` VARCHAR(255) NOT NULL DEFAULT '',
    `rc_doc` VARCHAR(255) NOT NULL DEFAULT '',
    `uploaded_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `license_file` VARCHAR(255) DEFAULT NULL,
    `rc_file` VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`document_id`),
    KEY `idx_vehdoc_driver` (`driver_id`),
    CONSTRAINT `fk_vehdoc_driver` FOREIGN KEY (`driver_id`) REFERENCES `tbl_driver` (`driver_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table 5: tbl_trip
-- Description: Stores active and completed safe ride journeys
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS `tbl_trip` (
    `trip_id` INT(11) NOT NULL AUTO_INCREMENT,
    `trip_uuid` CHAR(36) NOT NULL,
    `passenger_id` BIGINT(20) NOT NULL,
    `driver_id` INT(11) NOT NULL,
    `start_location` VARCHAR(100) NOT NULL DEFAULT 'Current Boarding Point',
    `end_location` VARCHAR(100) DEFAULT NULL,
    `start_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `end_time` DATETIME DEFAULT NULL,
    `status` VARCHAR(15) NOT NULL DEFAULT 'Ongoing',
    `pickup_location_name` VARCHAR(255) NOT NULL DEFAULT 'Current Location',
    `pickup_latitude` DOUBLE NOT NULL DEFAULT 9.6843,
    `pickup_longitude` DOUBLE NOT NULL DEFAULT 76.6853,
    `drop_location_name` VARCHAR(255) DEFAULT NULL,
    `drop_latitude` DOUBLE DEFAULT NULL,
    `drop_longitude` DOUBLE DEFAULT NULL,
    `live_latitude` DOUBLE NOT NULL DEFAULT 9.6843,
    `live_longitude` DOUBLE NOT NULL DEFAULT 76.6853,
    `live_updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `share_token` CHAR(36) NOT NULL,
    PRIMARY KEY (`trip_id`),
    UNIQUE KEY `uk_trip_uuid` (`trip_uuid`),
    UNIQUE KEY `uk_trip_share` (`share_token`),
    KEY `idx_trip_passenger` (`passenger_id`),
    KEY `idx_trip_driver` (`driver_id`),
    CONSTRAINT `fk_trip_driver` FOREIGN KEY (`driver_id`) REFERENCES `tbl_driver` (`driver_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table 6: tbl_rating_review
-- Description: Stores trip ratings, reviews and safety scores
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS `tbl_rating_review` (
    `rating_id` INT(11) NOT NULL AUTO_INCREMENT,
    `trip_id` INT(11) NOT NULL,
    `passenger_id` BIGINT(20) NOT NULL,
    `driver_id` INT(11) NOT NULL,
    `rating` SMALLINT(5) UNSIGNED NOT NULL DEFAULT 5,
    `review` TEXT DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `driving_safety_rating` SMALLINT(5) UNSIGNED NOT NULL DEFAULT 5,
    `vehicle_cleanliness_rating` SMALLINT(5) UNSIGNED NOT NULL DEFAULT 5,
    `behavior_rating` SMALLINT(5) UNSIGNED NOT NULL DEFAULT 5,
    `fare_honesty_rating` SMALLINT(5) UNSIGNED NOT NULL DEFAULT 5,
    PRIMARY KEY (`rating_id`),
    UNIQUE KEY `uk_rating_trip` (`trip_id`),
    KEY `idx_rating_passenger` (`passenger_id`),
    KEY `idx_rating_driver` (`driver_id`),
    CONSTRAINT `fk_rating_trip` FOREIGN KEY (`trip_id`) REFERENCES `tbl_trip` (`trip_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_rating_driver` FOREIGN KEY (`driver_id`) REFERENCES `tbl_driver` (`driver_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table 7: tbl_complaint
-- Description: Stores passenger grievances against drivers
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS `tbl_complaint` (
    `complaint_id` INT(11) NOT NULL AUTO_INCREMENT,
    `complaint_uuid` CHAR(36) NOT NULL,
    `trip_id` INT(11) DEFAULT NULL,
    `passenger_id` BIGINT(20) NOT NULL,
    `driver_id` INT(11) NOT NULL,
    `category` VARCHAR(30) NOT NULL DEFAULT 'MISBEHAVIOR',
    `description` TEXT NOT NULL,
    `evidence_photo` VARCHAR(255) DEFAULT NULL,
    `status` VARCHAR(15) NOT NULL DEFAULT 'Pending',
    `admin_remarks` TEXT DEFAULT NULL,
    `penalty_points_deducted` INT(11) NOT NULL DEFAULT 5,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `resolved_at` DATETIME DEFAULT NULL,
    PRIMARY KEY (`complaint_id`),
    UNIQUE KEY `uk_complaint_uuid` (`complaint_uuid`),
    KEY `idx_complaint_trip` (`trip_id`),
    KEY `idx_complaint_passenger` (`passenger_id`),
    KEY `idx_complaint_driver` (`driver_id`),
    CONSTRAINT `fk_complaint_trip` FOREIGN KEY (`trip_id`) REFERENCES `tbl_trip` (`trip_id`) ON DELETE SET NULL,
    CONSTRAINT `fk_complaint_driver` FOREIGN KEY (`driver_id`) REFERENCES `tbl_driver` (`driver_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table 8: tbl_sos_alert
-- Description: Stores real-time distress signals & police dispatch
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS `tbl_sos_alert` (
    `sos_id` INT(11) NOT NULL AUTO_INCREMENT,
    `alert_uuid` CHAR(36) NOT NULL,
    `passenger_id` BIGINT(20) NOT NULL,
    `trip_id` INT(11) DEFAULT NULL,
    `driver_id` INT(11) DEFAULT NULL,
    `location` VARCHAR(100) NOT NULL DEFAULT 'Live GPS Distress Location',
    `latitude` DOUBLE NOT NULL DEFAULT 9.6843,
    `longitude` DOUBLE NOT NULL DEFAULT 76.6853,
    `location_name` VARCHAR(255) NOT NULL DEFAULT 'Live GPS Distress Location',
    `status` VARCHAR(15) NOT NULL DEFAULT 'Active',
    `admin_notes` TEXT DEFAULT NULL,
    `dispatched_services` VARCHAR(255) NOT NULL DEFAULT 'Local Police (112) & Emergency Contacts',
    `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `resolved_at` DATETIME DEFAULT NULL,
    PRIMARY KEY (`sos_id`),
    UNIQUE KEY `uk_sos_uuid` (`alert_uuid`),
    KEY `idx_sos_trip` (`trip_id`),
    KEY `idx_sos_passenger` (`passenger_id`),
    KEY `idx_sos_driver` (`driver_id`),
    CONSTRAINT `fk_sos_trip` FOREIGN KEY (`trip_id`) REFERENCES `tbl_trip` (`trip_id`) ON DELETE SET NULL,
    CONSTRAINT `fk_sos_driver` FOREIGN KEY (`driver_id`) REFERENCES `tbl_driver` (`driver_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------
-- Table 9: tbl_incident_report
-- Description: Stores formal accident & safety hazard reports
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS `tbl_incident_report` (
    `incident_id` INT(11) NOT NULL AUTO_INCREMENT,
    `incident_uuid` CHAR(36) NOT NULL,
    `passenger_id` BIGINT(20) NOT NULL,
    `trip_id` INT(11) DEFAULT NULL,
    `incident_type` VARCHAR(30) NOT NULL DEFAULT 'Unsafe Driving',
    `description` TEXT NOT NULL,
    `status` VARCHAR(15) NOT NULL DEFAULT 'Pending',
    `reported_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`incident_id`),
    UNIQUE KEY `uk_incident_uuid` (`incident_uuid`),
    KEY `idx_incident_trip` (`trip_id`),
    KEY `idx_incident_passenger` (`passenger_id`),
    CONSTRAINT `fk_incident_trip` FOREIGN KEY (`trip_id`) REFERENCES `tbl_trip` (`trip_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
