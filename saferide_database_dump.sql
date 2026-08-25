-- --------------------------------------------------------
-- SafeRide: Complete MySQL Database Dump
-- Compatible with MySQL 8.x, MariaDB & phpMyAdmin
-- --------------------------------------------------------

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';
SET time_zone = '+00:00';

-- Table structure for `auth_group`
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for `auth_group_permissions`
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for `auth_permission`
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `auth_permission`
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
  (1, 'Can add log entry', 1, 'add_logentry'),
  (2, 'Can change log entry', 1, 'change_logentry'),
  (3, 'Can delete log entry', 1, 'delete_logentry'),
  (4, 'Can view log entry', 1, 'view_logentry'),
  (5, 'Can add permission', 3, 'add_permission'),
  (6, 'Can change permission', 3, 'change_permission'),
  (7, 'Can delete permission', 3, 'delete_permission'),
  (8, 'Can view permission', 3, 'view_permission'),
  (9, 'Can add group', 2, 'add_group'),
  (10, 'Can change group', 2, 'change_group'),
  (11, 'Can delete group', 2, 'delete_group'),
  (12, 'Can view group', 2, 'view_group'),
  (13, 'Can add content type', 4, 'add_contenttype'),
  (14, 'Can change content type', 4, 'change_contenttype'),
  (15, 'Can delete content type', 4, 'delete_contenttype'),
  (16, 'Can view content type', 4, 'view_contenttype'),
  (17, 'Can add session', 5, 'add_session'),
  (18, 'Can change session', 5, 'change_session'),
  (19, 'Can delete session', 5, 'delete_session'),
  (20, 'Can view session', 5, 'view_session'),
  (21, 'Can add user', 14, 'add_user'),
  (22, 'Can change user', 14, 'change_user'),
  (23, 'Can delete user', 14, 'delete_user'),
  (24, 'Can view user', 14, 'view_user'),
  (25, 'Can add Admin', 6, 'add_admin'),
  (26, 'Can change Admin', 6, 'change_admin'),
  (27, 'Can delete Admin', 6, 'delete_admin'),
  (28, 'Can view Admin', 6, 'view_admin'),
  (29, 'Can add Driver', 8, 'add_driver'),
  (30, 'Can change Driver', 8, 'change_driver'),
  (31, 'Can delete Driver', 8, 'delete_driver'),
  (32, 'Can view Driver', 8, 'view_driver'),
  (33, 'Can add Passenger', 10, 'add_passenger'),
  (34, 'Can change Passenger', 10, 'change_passenger'),
  (35, 'Can delete Passenger', 10, 'delete_passenger'),
  (36, 'Can view Passenger', 10, 'view_passenger'),
  (37, 'Can add Trip', 13, 'add_trip'),
  (38, 'Can change Trip', 13, 'change_trip'),
  (39, 'Can delete Trip', 13, 'delete_trip'),
  (40, 'Can view Trip', 13, 'view_trip'),
  (41, 'Can add SOS Alert', 12, 'add_sosalert'),
  (42, 'Can change SOS Alert', 12, 'change_sosalert'),
  (43, 'Can delete SOS Alert', 12, 'delete_sosalert'),
  (44, 'Can view SOS Alert', 12, 'view_sosalert'),
  (45, 'Can add Rating & Review', 11, 'add_ratingreview'),
  (46, 'Can change Rating & Review', 11, 'change_ratingreview'),
  (47, 'Can delete Rating & Review', 11, 'delete_ratingreview'),
  (48, 'Can view Rating & Review', 11, 'view_ratingreview'),
  (49, 'Can add Incident Report', 9, 'add_incidentreport'),
  (50, 'Can change Incident Report', 9, 'change_incidentreport'),
  (51, 'Can delete Incident Report', 9, 'delete_incidentreport'),
  (52, 'Can view Incident Report', 9, 'view_incidentreport'),
  (53, 'Can add Complaint', 7, 'add_complaint'),
  (54, 'Can change Complaint', 7, 'change_complaint'),
  (55, 'Can delete Complaint', 7, 'delete_complaint'),
  (56, 'Can view Complaint', 7, 'view_complaint'),
  (57, 'Can add Vehicle Document', 15, 'add_vehicledocuments'),
  (58, 'Can change Vehicle Document', 15, 'change_vehicledocuments'),
  (59, 'Can delete Vehicle Document', 15, 'delete_vehicledocuments'),
  (60, 'Can view Vehicle Document', 15, 'view_vehicledocuments');

-- Table structure for `django_admin_log`
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_tbl_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_tbl_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for `django_content_type`
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `django_content_type`
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
  (1, 'admin', 'logentry'),
  (2, 'auth', 'group'),
  (3, 'auth', 'permission'),
  (4, 'contenttypes', 'contenttype'),
  (6, 'core', 'admin'),
  (7, 'core', 'complaint'),
  (8, 'core', 'driver'),
  (9, 'core', 'incidentreport'),
  (10, 'core', 'passenger'),
  (11, 'core', 'ratingreview'),
  (12, 'core', 'sosalert'),
  (13, 'core', 'trip'),
  (14, 'core', 'user'),
  (15, 'core', 'vehicledocuments'),
  (5, 'sessions', 'session');

-- Table structure for `django_migrations`
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `django_migrations`
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
  (1, 'contenttypes', '0001_initial', '2026-08-23 04:08:46.738823'),
  (2, 'contenttypes', '0002_remove_content_type_name', '2026-08-23 04:08:47.229719'),
  (3, 'auth', '0001_initial', '2026-08-23 04:08:48.951876'),
  (4, 'auth', '0002_alter_permission_name_max_length', '2026-08-23 04:08:49.511361'),
  (5, 'auth', '0003_alter_user_email_max_length', '2026-08-23 04:08:49.539380'),
  (6, 'auth', '0004_alter_user_username_opts', '2026-08-23 04:08:49.578655'),
  (7, 'auth', '0005_alter_user_last_login_null', '2026-08-23 04:08:49.607380'),
  (8, 'auth', '0006_require_contenttypes_0002', '2026-08-23 04:08:49.634692'),
  (9, 'auth', '0007_alter_validators_add_error_messages', '2026-08-23 04:08:49.669077'),
  (10, 'auth', '0008_alter_user_username_max_length', '2026-08-23 04:08:49.693753'),
  (11, 'auth', '0009_alter_user_last_name_max_length', '2026-08-23 04:08:49.704973'),
  (12, 'auth', '0010_alter_group_name_max_length', '2026-08-23 04:08:49.782889'),
  (13, 'auth', '0011_update_proxy_permissions', '2026-08-23 04:08:49.800425'),
  (14, 'auth', '0012_alter_user_first_name_max_length', '2026-08-23 04:08:49.813306'),
  (15, 'core', '0001_initial', '2026-08-23 04:09:01.390470'),
  (16, 'admin', '0001_initial', '2026-08-23 04:09:02.741435'),
  (17, 'admin', '0002_logentry_remove_auto_add', '2026-08-23 04:09:02.853832'),
  (18, 'admin', '0003_logentry_add_action_flag_choices', '2026-08-23 04:09:02.884041'),
  (19, 'sessions', '0001_initial', '2026-08-23 04:09:03.069760'),
  (20, 'core', '0002_alter_ratingreview_rating_alter_sosalert_latitude_and_more', '2026-08-24 11:22:32.963314'),
  (21, 'core', '0003_trip_boarding_address_trip_boarding_latitude_and_more', '2026-08-24 11:27:08.791539');

-- Table structure for `django_session`
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `django_session`
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
  ('056s5h3d92ft7fqvxzbyvz8121lrqy1s', '.eJxVjMsOwiAQRf-FtSE8Bhlcuu83EB6DVA0kpV0Z_12bdKHbe865L-bDtla_DVr8nNmFScNOv2MM6UFtJ_ke2q3z1Nu6zJHvCj_o4FPP9Lwe7t9BDaN-a1B0zs5aAQaVFVkrKYpJOiAgGK2guBQcuIhRg5KWQFiDEYsrSBaBvT_OLzas:1wyTVO:Qs29oMJiNMvYPwRro4Uhtq62m92z5WmUGq4fFZNfkHU', '2026-09-07 12:10:22.077038'),
  ('0um6jl3shvpqg1wvatfjitdv61hciu1j', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyMcs:jsBeQ6boB5uxSTYnC-hofx01_cr49QQyh59a6Cf2gcE', '2026-09-07 04:49:38.189401'),
  ('117c0fc2cu80psur5aj98owp9ancoz63', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyA2o:W2JjjetRkbWZhV4uyBHiAFSDd1fm8U8g9_iZWKHi8Yw', '2026-09-06 15:23:34.731374'),
  ('1c454z5ylbio0brtt4vvsjgk6i38nzxn', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wxzpx:SEQ69Fz-l_h67QsvwPeslCZMCtCUylIzkGKb5bA7zNk', '2026-09-06 04:29:37.778256'),
  ('1j1fndzo9pnox04gl19nybfh20y20hta', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wy9Ra:pUezWVfvWqqYgEdlUgkDdbe4EsdezWCwhq5C4-Fu0Ac', '2026-09-06 14:45:06.045986'),
  ('1w158s9klq8l3ojd6c2cbjuusro4o4db', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9zk:5Ze5thDLEdhmjEiYkKoqIdgG4T7N7d5h0ILCYcxZEzw', '2026-09-06 15:20:24.295426'),
  ('1xmevkmrozjicwuzggoxcaob5vakvdql', '.eJxVjMsOgjAQRf-la9MwpTDUpXu_oZlHa1EDCYWV8d-VhIVu7znnvkykbS1xq2mJo5qzgc6cfkcmeaRpJ3qn6TZbmad1Gdnuij1otddZ0_NyuH8HhWr51qTA2FNGpJRJG2YCUJd9K67rW0EfOgzELmEQDyA9ZG5IBwcwYCbz_gAyBDiy:1wyTa9:tmXW_CHOXMXzv8ooc8Gn1xjBtFK2EeVBPVx43MbLIsg', '2026-09-07 12:15:17.455298'),
  ('2lofcv9cue42bnpchoy47y0egjrrp5gr', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyAUg:TNHb0NXoF1GatMaE4yFdkrGEHmjoZSokmonN-D8EFpw', '2026-09-06 15:52:22.099990'),
  ('3j3zy1dlh2lu2v5ddxcdbxnfsty9sbb2', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wySd8:PI350mqNsN7rEs4N6E47tE72vAPtmVLmjTqFwcfg_Zg', '2026-09-07 11:14:18.145975'),
  ('3sasy4y26o2oc75p4vhonmk5w7j1shy4', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyA6j:uiGBFxAu1_148syIuBIFg9Ubb6bsGwdjfP4NacJHMUM', '2026-09-06 15:27:37.691089'),
  ('43xqga4hszrstgp6ajvt1icsssveuegl', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySla:NeOOZ_nNF2A0rloUc0tJ15FoE-oL6dmVLpZ1-DPrOyI', '2026-09-07 11:23:02.700787'),
  ('4v394iyzbiag8ycwzzbk9u78hkuh1kmj', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyMcx:nxWN7iHaB6xxum8pkARZeQuHDKjqUWakcDzphgkPdL8', '2026-09-07 04:49:43.080869'),
  ('518o1qx6zkgeroj34utnpwa04cav2jyn', '.eJxVjMsOwiAQRf-FtSEMDBRcuvcbyPCSqoGktCvjv2uTLnR7zzn3xTxta_XbyIufEzszZKffLVB85LaDdKd26zz2ti5z4LvCDzr4taf8vBzu30GlUb81oZ2cdmgT5RKtkEGZAqgnaUCAyKiLciWSkmSCgWS1pYJRK8waJAj2_gDNTTcQ:1wy9C5:XN4qCWucoRJwRtf3sodTe-A94VD1pzxoOoHw5J-fujA', '2026-09-06 14:29:05.217100'),
  ('56cuef5lggp8fiqi2033cc51yagmy009', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySro:EXybRpb2iRhhIJMXdcCKO2ncGjLxOizZ6QPywRYginI', '2026-09-07 11:29:28.421456'),
  ('5dx0r9l8tjxrezvpacc0y57o1uepk9oy', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wy00k:6pyl6UmMDCdMsAQUWZVbKtTDYCIcqv-FNGc0Wsf_S4c', '2026-09-06 04:40:46.532379'),
  ('60ydfqzhlbo4pz58n1vqcw6ocqvi650a', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYHM:U5wbMUcs2CzkrnitZ6COvqu0xKUcOqnP0cuycpYRf_w', '2026-09-07 17:16:12.018449'),
  ('6dj2uu7msggpslhvcjezotu5afep0bw9', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyTjk:tK1ZtYAe_ox1TIoTBLusaCMoWK6EVuUSo9yELHTl6qc', '2026-09-07 12:25:12.302661'),
  ('7ln85k2orf7sixr2kyuq5h9l1j4kyyen', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wy9Uh:LWClfDF0w08DQsMgnTZzvXsJOkciJS7EzHzPA6mt2Nk', '2026-09-06 14:48:19.780988'),
  ('9gn4fmlc3wy50grupkpsfj3kyacknot0', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyALL:GNZiCPPSLkruPUnNYRDaeYsdurI905KjyRifpHRP12k', '2026-09-06 15:42:43.196797'),
  ('9m8ejpjkvdkservdvgjag4pm9yeid4yu', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wy9b7:ufiI3GjJ9pyA7iwS9ikx5dQCx4DoxtAI704_GjJKFbo', '2026-09-06 14:54:57.330718'),
  ('9rp4tln4enmxb7xkajpk73lu9lzttzon', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wxzry:f4ws0tQC-rr29Wm-WL3k-kQrtT6QrV86z0oeiSSEdQE', '2026-09-06 04:31:42.071054'),
  ('afmitdviimb3yuuvnpe6ngzqv7ypi5c7', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyABj:Q1exz5pp9kpvPcXWtT0zmPJlzVypNyl6ykehlq3w2VU', '2026-09-06 15:32:47.192494'),
  ('bpjml9zfr9vt504sp0kqdfssiz4o8wcr', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyA10:0XNShwHMajARMk16qRt8uj_PqS62ixcv84ipp_sMRMI', '2026-09-06 15:21:42.066173'),
  ('czs8le79obqx2zq3yuqv9if2628tqzdd', '.eJxVjMsOwiAQRf-FtSEgMIBL9_0GMsNDqoYmpV0Z_11JutDVTe45OS8WcN9q2Htew5zYhUnDTr8nYXzkNki6Y7stPC5tW2fiQ-EH7XxaUn5eD_cvULHX0RUoidB9B5TRVhRZkvZgfSFvz5GScqDIIhalpXcAUpZitNcCrHHA3h_34zci:1wyTEx:0Y3NBPNlR5DgsWfCUcn7WbBMng4002ZbxS9lXI3Stxw', '2026-09-07 11:53:23.279229'),
  ('drzonki1pnbb64z4m8skgx0f34ao45xm', '.eJxVjDsOwjAQBe_iGln4x7KU9JzBWu86OIBsKU4qxN1JpBTQvpl5bxVpmUtcep7iKOqiTFCH3zERP3PdiDyo3pvmVudpTHpT9E67vjXJr-vu_h0U6mWtBzAZHUO2ICIeBuOctyGRAyvkDZMTQIsYfGZAMIboZJlXchbCo_p8AQpkOAg:1wyTMs:fCahUvqCadTdWxc7Tyl7N52rp5N_vM6ZcpFtieCOp0c', '2026-09-07 12:01:34.428591'),
  ('e013g4q2dwrixenqvx4gyu89ul2gm89g', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wxzyy:QDgAydsXkzHGYaZORh9UBFj__DevZECRq1FhezF1H_k', '2026-09-06 04:38:56.726232'),
  ('elwsz8awyv8fuw94oksyl5srghqgr6ga', '.eJxVjDsOwjAQBe_iGlk2_iWU9DmDtetd4wCypTipEHeHSCmgfTPzXiLCtpa4dV7iTOIitDj9bgjpwXUHdId6azK1ui4zyl2RB-1yasTP6-H-HRTo5VtboJSYbTLsRuWsIq_0WYcADgYgy0GZDD5nlQKgQzSAYAbGnEfPisX7AwPqOTw:1wyN9J:QcIF9XWTOQHzQdNmJoSQWcZ_KWbhTiUjtAvSSrSL4mU', '2026-09-07 05:23:09.313583'),
  ('er6c6mtqwodi19lckad4uiy9dtmu19ps', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wxziG:DLV9apzT1l4rbs4NNO7NWOznBoJSdp0dn--FsmhFYdk', '2026-09-06 04:21:40.621555'),
  ('gf482ke5y6h75lgtwogfjvxobyo7pbrk', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyMcv:2PNJQNRR7zbS-CRoUYFIN_VJZ3tIsjf0IxdKW0-bsQ0', '2026-09-07 04:49:41.707938'),
  ('hazhvvwhzah1xune0rfuvaujfc952c2r', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyN03:AGLYh5kLV6-P74rVywgE6u4emiAAwKUWbw83us8iJJ4', '2026-09-07 05:13:35.991653'),
  ('hbkl7esfwqficlecehuddeciny6yfp6a', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9vD:-kxkDOpHL0SSenicoXMjfX1sjqxokPw0pwwLXS9cEQM', '2026-09-06 15:15:43.621277'),
  ('izkrlq5cqlwch5xr8xs9594a9fcsqx7j', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyTez:rEShX6TDrZi6YrJG2pyC8vjDTCoRvG9jIZliFMUjWlQ', '2026-09-07 12:20:17.786114'),
  ('k36tetd2ubxhdjzorpc0895j3x9rf5b0', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySlK:QWOf837xWXUOtUpPZSYRxbyc9AthhqrkAVeV3bKTs8A', '2026-09-07 11:22:46.581981'),
  ('kepf622d6k7bhnx5oxlvjhb47tgjjc3u', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySfW:J08bNGTDM4KvGcdJvtw9LvnYhmFEJ30Us3uSvgYmbJE', '2026-09-07 11:16:46.643680'),
  ('lk7w3ezejmafbcg7kc6at0vomhpoh5ik', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyA6H:2qcp5OQwmzSM1o0rhvRm4jmguDHYDRHzfTOEXvJ-ThQ', '2026-09-06 15:27:09.201631'),
  ('lyg3zfkdoxnoy1z0f97q3ykf6zkzp1bs', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9lU:vci5YnQfyMX6eWEUlBjxrGr1MRNLeUdkjNgekfJp9_k', '2026-09-06 15:05:40.040081'),
  ('obzmx18jcao7q5elbw9z28729eznt4gj', '.eJxVjMsOwiAQRf-FtSEMDBRcuvcbyPCSqoGktCvjv2uTLnR7zzn3xTxta_XbyIufEzszZKffLVB85LaDdKd26zz2ti5z4LvCDzr4taf8vBzu30GlUb81oZ2cdmgT5RKtkEGZAqgnaUCAyKiLciWSkmSCgWS1pYJRK8waJAj2_gDNTTcQ:1wyAFc:qtoBC7-TmnnOp-ZTH8M7spoQz49XWOdJQzng8xZ5ahA', '2026-09-06 15:36:48.732936'),
  ('okjb6q6v2qomlo9to64ago03apnkpmoq', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9ut:rUbBH9iA1R1OkwCmH_4U8_OXTRPHOXp7ZHNBDsdK7gE', '2026-09-06 15:15:23.998029'),
  ('p8px40428f24xry9cjozpf12i06fikms', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYHS:7HYguUp9vOzDm6oCacOXQ1RW-hpSLE3g-8OSyB4QtDY', '2026-09-07 17:16:18.689803'),
  ('pgrx18qve2kk5cwrlyjruhftq08ambf0', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySsU:KwK4Yo2HMF9blVOwaHXDERRF92d88PDPaln8X7PXE2M', '2026-09-07 11:30:10.435936'),
  ('q3j05pgzovkzbb8z2tcok0urodu0dn80', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyAT0:FYcp77o4sPxw99SHXisQ1yEVKWd_6Hd02WlG8E6GNDc', '2026-09-06 15:50:38.753726'),
  ('qjybvro9r4128aqo6qfdd2zutd0ywejs', '.eJxVjMsOwiAQRf-FtSEMDBRcuvcbyPCSqoGktCvjv2uTLnR7zzn3xTxta_XbyIufEzszZKffLVB85LaDdKd26zz2ti5z4LvCDzr4taf8vBzu30GlUb81oZ2cdmgT5RKtkEGZAqgnaUCAyKiLciWSkmSCgWS1pYJRK8waJAj2_gDNTTcQ:1wxzoU:XwdXXGWpe4pwyAA4lzLFrniGh2D1dcdVu_XilKpsG3I', '2026-09-06 04:28:06.837610'),
  ('rqih6nqnhife6lp3p50i7w0j47v1h9g7', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9rI:FVbnfwybMh1hYIMoI-5VcAglJSnlMhx5iQHwmrfGnC0', '2026-09-06 15:11:40.280175'),
  ('t14tfa2fwubcn74ygopynma1coenninz', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySek:RxXdQ9VoUCMbbCvX4r_UjKc6WYUJs2YFUL1nUH2HZHE', '2026-09-07 11:15:58.177099'),
  ('t5gcss88petw6tu5bfv5f19xrd5s3xre', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyABl:YNV3vUM0XRn22_p1zirBrEX_09wFQzvMKCsROWsEESU', '2026-09-06 15:32:49.026076'),
  ('t9825qhow33pluxhj05002ga0b8ofnoi', '.eJxVjMsOwiAQRf-FtSEMDBRcuvcbyPCSqoGktCvjv2uTLnR7zzn3xTxta_XbyIufEzszZKffLVB85LaDdKd26zz2ti5z4LvCDzr4taf8vBzu30GlUb81oZ2cdmgT5RKtkEGZAqgnaUCAyKiLciWSkmSCgWS1pYJRK8waJAj2_gDNTTcQ:1wyAF0:mzkAoMzBb6fO3wNC93xTJfv-dK1cSxcxS-yoBQa4dtE', '2026-09-06 15:36:10.420736'),
  ('tgjvosq7v8a7rxgzmh1vha20nxxdodzc', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySiu:4KM928IikNTqy7gqzS2290IMgeLw8fqFR2X9evfJ5yo', '2026-09-07 11:20:16.562687'),
  ('tjuzwuhfk2k30tpa2a9gtu0mbh183diw', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyABm:JH6hZ7OVK5OH6IQtJ4q8jNjxFsFbZOfB-r2v8r3c5Z4', '2026-09-06 15:32:50.658393'),
  ('u23s5k8azkmsssfjqb8d20980y6fk6zh', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyAL0:LfZb-obZt4Lm0QKSXnCFjT_1LGT5oONs9xMMGfcQ3Z0', '2026-09-06 15:42:22.593628'),
  ('ua7kivsa7uy9fkkd3tou5c46k3lgf5ng', '.eJxVjMsOwiAQRf-FtSEMDBRcuvcbyPCSqoGktCvjv2uTLnR7zzn3xTxta_XbyIufEzszZKffLVB85LaDdKd26zz2ti5z4LvCDzr4taf8vBzu30GlUb81oZ2cdmgT5RKtkEGZAqgnaUCAyKiLciWSkmSCgWS1pYJRK8waJAj2_gDNTTcQ:1wyAHD:5rmVT1bOLlucE0Ta485d3dRsR4pSru-V6MWELvGscXs', '2026-09-06 15:38:27.528843'),
  ('ufyxoolam0n5finoi3ifsxt3s76wvk7w', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYHR:yY-uAYwrGTvJNSP-wKfDsqx-O_Ym78UBHLNYOi5kIAc', '2026-09-07 17:16:17.506959'),
  ('up1590xdbm1hwrjsa4o6offpvjkcc1x1', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wxzjV:FmPqt80Q-607Ih5w_LlXb26gAfwen0R-N_73BZkL3L0', '2026-09-06 04:22:57.139573'),
  ('vbdsyo47ih3yjkbha6ezpgmkt88mbs6q', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9lV:-PRnr9SIFLzz2nruFDBPzVAcXex_KhnX66MgOL_Z1jo', '2026-09-06 15:05:41.264685'),
  ('x845v1axmaoyu6cqelgbonwqm1t0hsj2', '.eJxVjDsOwjAQBe_iGlk2_iWU9DmDtetd4wCypTipEHeHSCmgfTPzXiLCtpa4dV7iTOIitDj9bgjpwXUHdId6azK1ui4zyl2RB-1yasTP6-H-HRTo5VtboJSYbTLsRuWsIq_0WYcADgYgy0GZDD5nlQKgQzSAYAbGnEfPisX7AwPqOTw:1wyN9H:Rq8dHa3RtPMyfu3m5HTDqjr1sZMKKtEjuGWbuWELfVc', '2026-09-07 05:23:07.984569'),
  ('y4l9k23ky1w4o4elmhuzymbkezqxrotc', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wySf2:DWxwDXJMfgKVOD1OfY1XzOl7mmVIHJAljZv_GCC_seY', '2026-09-07 11:16:16.326653'),
  ('y5004ok0k1mras7le6qtue3ih5a5gdwf', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySfq:YuQgVBXZmX-rlofGI8AvWgWFKvj5Thia3KcgtDdXGew', '2026-09-07 11:17:06.129541'),
  ('ydmclhufbwtwspemcmavjej025q3dn6r', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyA9I:Oxx8dumEB_DmcxuqUpPirY218xxPRrwP1QPfziu7AIM', '2026-09-06 15:30:16.716132'),
  ('yu2nkrbhy59t3g3jl951m605fvzp2qvn', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy88y:X1JiT2vW7UhY9yQdKodSh-p8bnEkfprouh6gpMFoimc', '2026-09-06 13:21:48.024768'),
  ('zdakb2gdrsu6p7dkxw5fruttn89ktdac', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyThY:slZT6jqMBiiNg9Dd24QjCAQ3j-28IJ3RZcT2gFMb1ZA', '2026-09-07 12:22:56.759036');

-- Table structure for `tbl_admin`
DROP TABLE IF EXISTS `tbl_admin`;
CREATE TABLE `tbl_admin` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `tbl_admin_user_id_11a4382e_fk_tbl_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_admin`
INSERT INTO `tbl_admin` (`admin_id`, `name`, `email`, `password`, `user_id`) VALUES
  (1, 'SafeRide Administrator', 'admin@saferide.org', 'pbkdf2_sha256$1500000$NExKjw2djokVVBFV4cepBk$aG7FQtmI7qBTqhS/GqNasGiqQgB0B98h5tsospk5CHg=', 1);

-- Table structure for `tbl_complaint`
DROP TABLE IF EXISTS `tbl_complaint`;
CREATE TABLE `tbl_complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `complaint_uuid` char(32) NOT NULL,
  `description` longtext NOT NULL,
  `status` varchar(15) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `category` varchar(30) NOT NULL,
  `evidence_photo` varchar(100) DEFAULT NULL,
  `admin_remarks` longtext DEFAULT NULL,
  `penalty_points_deducted` int(11) NOT NULL,
  `resolved_at` datetime(6) DEFAULT NULL,
  `passenger_id` bigint(20) NOT NULL,
  `driver_id` int(11) NOT NULL,
  `trip_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`),
  UNIQUE KEY `complaint_uuid` (`complaint_uuid`),
  KEY `tbl_complaint_passenger_id_897bb18a_fk_tbl_user_id` (`passenger_id`),
  KEY `tbl_complaint_driver_id_e2fa4c61_fk_tbl_driver_driver_id` (`driver_id`),
  KEY `tbl_complaint_trip_id_da69c575_fk_tbl_trip_trip_id` (`trip_id`),
  CONSTRAINT `tbl_complaint_driver_id_e2fa4c61_fk_tbl_driver_driver_id` FOREIGN KEY (`driver_id`) REFERENCES `tbl_driver` (`driver_id`),
  CONSTRAINT `tbl_complaint_passenger_id_897bb18a_fk_tbl_user_id` FOREIGN KEY (`passenger_id`) REFERENCES `tbl_user` (`id`),
  CONSTRAINT `tbl_complaint_trip_id_da69c575_fk_tbl_trip_trip_id` FOREIGN KEY (`trip_id`) REFERENCES `tbl_trip` (`trip_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_complaint`
INSERT INTO `tbl_complaint` (`complaint_id`, `complaint_uuid`, `description`, `status`, `created_at`, `category`, `evidence_photo`, `admin_remarks`, `penalty_points_deducted`, `resolved_at`, `passenger_id`, `driver_id`, `trip_id`) VALUES
  (1, 'a29b3d4ce71640b084b05dc9eee77605', 'Driver demanded excess fare above meter rate during night commute and refused to use standard fare table.', 'Pending', '2026-08-23 04:09:30.663305', 'OVERCHARGING', '', NULL, 5, NULL, 3, 4, NULL);

-- Table structure for `tbl_driver`
DROP TABLE IF EXISTS `tbl_driver`;
CREATE TABLE `tbl_driver` (
  `driver_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `license_number` varchar(30) NOT NULL,
  `vehicle_number` varchar(20) NOT NULL,
  `vehicle_type` varchar(20) NOT NULL,
  `verification_status` varchar(15) NOT NULL,
  `qr_code` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `experience_years` int(10) unsigned NOT NULL CHECK (`experience_years` >= 0),
  `verification_notes` longtext DEFAULT NULL,
  `verified_at` datetime(6) DEFAULT NULL,
  `verification_token` char(32) NOT NULL,
  `reputation_score` double NOT NULL,
  `total_trips` int(10) unsigned NOT NULL CHECK (`total_trips` >= 0),
  `average_rating` double NOT NULL,
  `driver_photo` varchar(100) DEFAULT NULL,
  `license_doc` varchar(100) DEFAULT NULL,
  `id_proof_doc` varchar(100) DEFAULT NULL,
  `police_clearance_doc` varchar(100) DEFAULT NULL,
  `qr_code_image` varchar(100) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`driver_id`),
  UNIQUE KEY `phone_number` (`phone_number`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `license_number` (`license_number`),
  UNIQUE KEY `vehicle_number` (`vehicle_number`),
  UNIQUE KEY `verification_token` (`verification_token`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `tbl_driver_user_id_592ecf89_fk_tbl_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_driver`
INSERT INTO `tbl_driver` (`driver_id`, `name`, `phone_number`, `email`, `license_number`, `vehicle_number`, `vehicle_type`, `verification_status`, `qr_code`, `password`, `experience_years`, `verification_notes`, `verified_at`, `verification_token`, `reputation_score`, `total_trips`, `average_rating`, `driver_photo`, `license_doc`, `id_proof_doc`, `police_clearance_doc`, `qr_code_image`, `user_id`) VALUES
  (1, 'Rajesh Kumar', '+91 9447182930', 'driver_rajesh@saferide.org', 'KL-05-20180004521', 'KL-05-AT-4455', 'auto', 'Verified', '/media/driver_qrcodes/qr_KL-05-20180004521_1.png', 'pbkdf2_sha256$1500000$s5BmTCJ9FeyZ4JyEttwO4e$cEpT43Xask8eKJzZNV3EDYym2boP8nMx/oXqwPb3yVA=', 7, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:48.390508', '37644fd208ec44d2b0a7ff224b551ad2', 100.0, 647, 5.0, '', '', '', '', 'driver_qrcodes/qr_KL-05-20180004521_1.png', 4),
  (2, 'Anand Joseph', '+91 9847334455', 'driver_anand@saferide.org', 'KL-05-20150009812', 'KL-05-TX-1024', 'taxi', 'Verified', '/media/driver_qrcodes/qr_KL-05-20150009812_2.png', 'pbkdf2_sha256$1500000$dkJyokgiTgtFbgMGDbjEU0$C3eNLpcNqySs+AqI+dhM9VXq4uzqTnvDxv7w3PpESDY=', 9, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:50.023904', '25bab7460d5b4b9482b219dfc3d2f41d', 100.0, 418, 5.0, '', '', '', '', 'driver_qrcodes/qr_KL-05-20150009812_2.png', 5),
  (3, 'Suresh Babu', '+91 9745112233', 'driver_suresh@saferide.org', 'KL-05-20200003411', 'KL-05-CB-8890', 'cab', 'Verified', '/media/driver_qrcodes/qr_KL-05-20200003411_3.png', 'pbkdf2_sha256$1500000$brb2FYiWtSy8rvOH5f7Vf6$QdV6GdWFomxBJwXRzS7BRgklFl8GNcvaiVYGmjM22ek=', 4, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:51.542929', '58ce14e0766a4cf9b9c379f6bf63d7c3', 89.5, 215, 4.6, '', '', '', '', 'driver_qrcodes/qr_KL-05-20200003411_3.png', 6),
  (4, 'Vinod Mohan', '+91 9400223344', 'driver_vinod@saferide.org', 'KL-05-20240001290', 'KL-05-AT-9911', 'auto', 'Pending', NULL, 'pbkdf2_sha256$1500000$6PRFReWJH9t2mCrKibFcBs$Lq/+wjUfAI9MS316y/z0j+7/rr7EbcD9pWPCdaLXZV4=', 1, 'Awaiting physical RC verification', NULL, '0e0a406792c8431d8d60fca5a64937f6', 75.0, 12, 4.2, '', '', '', '', '', 7),
  (5, 'Pradeep Chandran', '+91 9447665544', 'driver_pradeep@saferide.org', 'KL-05-20170008821', 'KL-05-AT-7788', 'auto', 'Verified', '/media/driver_qrcodes/qr_KL-05-20170008821_5.png', 'pbkdf2_sha256$1500000$oFimqWMPwCCPV74BRTEpqY$8zZ0yR6pVxGISl5NdAoSHK7wYH6eol2RZonucWB66io=', 8, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:54.528353', '0e766821901b4928910dc447d77d3f1c', 95.0, 520, 4.85, '', '', '', '', 'driver_qrcodes/qr_KL-05-20170008821_5.png', 8),
  (6, 'Mathew Varghese', '+91 9847119988', 'driver_mathew@saferide.org', 'KL-35-20160007743', 'KL-35-TX-4521', 'taxi', 'Verified', '/media/driver_qrcodes/qr_KL-35-20160007743_6.png', 'pbkdf2_sha256$1500000$kJlNTxOE5ifRT86Q9Z7lZN$/S7btWVXsFbfnRDFO9OAaoEVZ6gdxGSaYz5APdMUvq4=', 10, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:56.223393', 'bbdfd1e9f4144ff9a01b84982d84d4d0', 98.5, 780, 4.95, '', '', '', '', 'driver_qrcodes/qr_KL-35-20160007743_6.png', 9),
  (7, 'Harikrishnan Nair', '+91 9745887766', 'driver_hari@saferide.org', 'KL-05-20190005512', 'KL-05-CB-3344', 'cab', 'Verified', '/media/driver_qrcodes/qr_KL-05-20190005512_7.png', 'pbkdf2_sha256$1500000$agqyrSDJwt9tnkWl7llvfv$1Jrc06hWqLQm3ve2smpWwXhUy2RwpvT0nwV6Vfty+Cc=', 5, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:57.933082', 'f0b8451da7bc4513bfc77f2d81048068', 91.0, 340, 4.75, '', '', '', '', 'driver_qrcodes/qr_KL-05-20190005512_7.png', 10),
  (8, 'Shaji Thomas', '+91 9495223311', 'driver_shaji@saferide.org', 'KL-05-20210006678', 'KL-05-EV-1205', 'cab', 'Verified', '/media/driver_qrcodes/qr_KL-05-20210006678_8.png', 'pbkdf2_sha256$1500000$GJA28sP6KSqf4PryyHEsqR$8GPdiyFDcwu4Iy9WRTRzmT9iNxBFqKDjAEcOV1gYz6c=', 3, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:59.567807', '4a2c531981b34fdf9ff44a04200ac786', 93.5, 195, 4.9, '', '', '', '', 'driver_qrcodes/qr_KL-05-20210006678_8.png', 11),
  (9, 'Anoop Rajan', '+91 9605443322', 'driver_anoop@saferide.org', 'KL-35-20230009988', 'KL-35-AT-6622', 'auto', 'Pending', NULL, 'pbkdf2_sha256$1500000$ssD832GhfdKZEYtyOPnq0x$MIy76IXtI6bMTbkWBn7UsBqxqOh1HLmPK3Ni3hMbqRk=', 2, 'Awaiting physical RC verification', NULL, '3e5008d550e845d0b84f6a3f1ae08d4a', 78.0, 45, 4.4, '', '', '', '', '', 12),
  (10, 'Deepak K. S.', '+91 9946115500', 'driver_deepak@saferide.org', 'KL-07-20140003321', 'KL-07-CB-9080', 'cab', 'Verified', '/media/driver_qrcodes/qr_KL-07-20140003321_10.png', 'pbkdf2_sha256$1500000$5MIo90sfowgYLJRQeHQTJW$Ru4NttqmuqCxj2GAYiYETKBW3OCzKlT9zaExapZr0lQ=', 11, 'Document verification completed and police clearance verified.', '2026-08-24 11:02:02.951171', '61147761bd0740e49e8c25ab9ea48e66', 97.0, 910, 4.92, '', '', '', '', 'driver_qrcodes/qr_KL-07-20140003321_10.png', 13);

-- Table structure for `tbl_incident_report`
DROP TABLE IF EXISTS `tbl_incident_report`;
CREATE TABLE `tbl_incident_report` (
  `incident_id` int(11) NOT NULL AUTO_INCREMENT,
  `incident_uuid` char(32) NOT NULL,
  `incident_type` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  `status` varchar(15) NOT NULL,
  `reported_at` datetime(6) NOT NULL,
  `passenger_id` bigint(20) NOT NULL,
  `trip_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`incident_id`),
  UNIQUE KEY `incident_uuid` (`incident_uuid`),
  KEY `tbl_incident_report_passenger_id_6f0682f6_fk_tbl_user_id` (`passenger_id`),
  KEY `tbl_incident_report_trip_id_8551fdd7_fk_tbl_trip_trip_id` (`trip_id`),
  CONSTRAINT `tbl_incident_report_passenger_id_6f0682f6_fk_tbl_user_id` FOREIGN KEY (`passenger_id`) REFERENCES `tbl_user` (`id`),
  CONSTRAINT `tbl_incident_report_trip_id_8551fdd7_fk_tbl_trip_trip_id` FOREIGN KEY (`trip_id`) REFERENCES `tbl_trip` (`trip_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_incident_report`
INSERT INTO `tbl_incident_report` (`incident_id`, `incident_uuid`, `incident_type`, `description`, `status`, `reported_at`, `passenger_id`, `trip_id`) VALUES
  (1, '4a68021c210f45f3aaf41ad331eb37f9', 'Unsafe Driving', 'Aggressive overtaking near steep turn on Pala highway.', 'Pending', '2026-08-23 04:09:30.835741', 2, NULL),
  (2, 'cee88eadb0af4baba58d488e87413eb6', 'Unsafe Driving', 'Driver skipped red signal', 'Pending', '2026-08-23 14:34:20.411746', 2, NULL),
  (3, '3d7f85fd4d9d475894cb252b68917f45', 'Unsafe Driving', 'Driver skipped red signal', 'Pending', '2026-08-23 14:35:10.825995', 2, NULL),
  (4, '34d18c86c8aa4bd79694e961c9693876', 'ACCIDENT', 'Vehicle had a minor collision on SH-32, passenger safe.', 'Pending', '2026-08-23 15:52:22.393230', 2, NULL);

-- Table structure for `tbl_passenger`
DROP TABLE IF EXISTS `tbl_passenger`;
CREATE TABLE `tbl_passenger` (
  `passenger_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `emergency_contact_1_name` varchar(100) DEFAULT NULL,
  `emergency_contact_1_phone` varchar(20) DEFAULT NULL,
  `emergency_contact_1_relation` varchar(50) DEFAULT NULL,
  `emergency_contact_2_name` varchar(100) DEFAULT NULL,
  `emergency_contact_2_phone` varchar(20) DEFAULT NULL,
  `emergency_contact_2_relation` varchar(50) DEFAULT NULL,
  `emergency_contact_3_name` varchar(100) DEFAULT NULL,
  `emergency_contact_3_phone` varchar(20) DEFAULT NULL,
  `emergency_contact_3_relation` varchar(50) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `profile_photo` varchar(100) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`passenger_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `tbl_passenger_user_id_eaa3b76d_fk_tbl_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_passenger`
INSERT INTO `tbl_passenger` (`passenger_id`, `name`, `email`, `phone_number`, `password`, `created_at`, `emergency_contact_1_name`, `emergency_contact_1_phone`, `emergency_contact_1_relation`, `emergency_contact_2_name`, `emergency_contact_2_phone`, `emergency_contact_2_relation`, `emergency_contact_3_name`, `emergency_contact_3_phone`, `emergency_contact_3_relation`, `address`, `profile_photo`, `user_id`) VALUES
  (1, 'Vyshnavi Venu', 'vyshnavi@sjcetpalai.ac.in', '+91 9847123456', 'pbkdf2_sha256$1500000$n0tjOBL02bEGRc0vFb7d2J$lc5mU91eR8yCW2vtc1iczntJtO2tlasbsqLGQR5YSeU=', '2026-08-23 04:09:12.705026', 'Venu Chandrasekharan Nair (Father)', '+91 9447012345', 'Parent', 'SJCET Security / Helpdesk', '+91 4822239700', 'Campus Security', NULL, NULL, 'Guardian', 'Palai, Kottayam, Kerala', '', 2),
  (2, 'Rahul Kurian', 'rahul.k@gmail.com', '+91 9895001122', 'pbkdf2_sha256$1500000$LqYbbCK759PfeVmuNI204T$PESJ7WpPXF74v1YAjBT3T7dzG25wVtFtt12NB79lmVE=', '2026-08-23 04:09:16.010659', 'Anita Kurian', '+91 9895009988', 'Sister', NULL, NULL, 'Friend', NULL, NULL, 'Guardian', 'Kottayam Road, Palai', '', 3),
  (3, 'SafeRide Administrator', 'admin@saferide.org', '', 'pbkdf2_sha256$1500000$qRYqFxO3ZarxP5AvwPWfUz$ogYbZLSETS1yGh0823BOTeFaZJ/82syi6O17QJ50jk4=', '2026-08-23 10:08:49.679458', NULL, NULL, 'Family', NULL, NULL, 'Friend', NULL, NULL, 'Guardian', NULL, '', 1),
  (4, '7874518415 178872446', 'vyshnavivenu2020@gmail.com', '/87/*98568', 'pbkdf2_sha256$1500000$7fyxwmE9Bt8CgagkA7msGs$IOnLqlG3N+oRYPxcM5p48SCv5svrlW8ih6gr+VkhRcQ=', '2026-08-24 10:58:40.215896', '4444', 'vyshnavi', 'Family', NULL, NULL, 'Friend', NULL, NULL, 'Guardian', NULL, '', 14),
  (5, 'Vyshnavi Venu', 'vyshnavi.e2e@saferide.org', '9846012345', 'pbkdf2_sha256$1500000$VISCCzMNxSBPOMRIhbeFGi$7KVnRNbhUiREEiNU1kjkU2f/uveWatk7YwoGl6k2mbA=', '2026-08-24 11:53:02.023916', NULL, NULL, 'Family', NULL, NULL, 'Friend', NULL, NULL, 'Guardian', NULL, '', 15);

-- Table structure for `tbl_rating_review`
DROP TABLE IF EXISTS `tbl_rating_review`;
CREATE TABLE `tbl_rating_review` (
  `rating_id` int(11) NOT NULL AUTO_INCREMENT,
  `rating` smallint(5) unsigned NOT NULL CHECK (`rating` >= 0),
  `review` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `driving_safety_rating` smallint(5) unsigned NOT NULL CHECK (`driving_safety_rating` >= 0),
  `vehicle_cleanliness_rating` smallint(5) unsigned NOT NULL CHECK (`vehicle_cleanliness_rating` >= 0),
  `behavior_rating` smallint(5) unsigned NOT NULL CHECK (`behavior_rating` >= 0),
  `fare_honesty_rating` smallint(5) unsigned NOT NULL CHECK (`fare_honesty_rating` >= 0),
  `driver_id` int(11) NOT NULL,
  `passenger_id` bigint(20) NOT NULL,
  `trip_id` int(11) NOT NULL,
  PRIMARY KEY (`rating_id`),
  UNIQUE KEY `trip_id` (`trip_id`),
  KEY `tbl_rating_review_driver_id_1195b985_fk_tbl_driver_driver_id` (`driver_id`),
  KEY `tbl_rating_review_passenger_id_d22b1515_fk_tbl_user_id` (`passenger_id`),
  CONSTRAINT `tbl_rating_review_driver_id_1195b985_fk_tbl_driver_driver_id` FOREIGN KEY (`driver_id`) REFERENCES `tbl_driver` (`driver_id`),
  CONSTRAINT `tbl_rating_review_passenger_id_d22b1515_fk_tbl_user_id` FOREIGN KEY (`passenger_id`) REFERENCES `tbl_user` (`id`),
  CONSTRAINT `tbl_rating_review_trip_id_48c2b492_fk_tbl_trip_trip_id` FOREIGN KEY (`trip_id`) REFERENCES `tbl_trip` (`trip_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_rating_review`
INSERT INTO `tbl_rating_review` (`rating_id`, `rating`, `review`, `created_at`, `driving_safety_rating`, `vehicle_cleanliness_rating`, `behavior_rating`, `fare_honesty_rating`, `driver_id`, `passenger_id`, `trip_id`) VALUES
  (9, 5, 'Very polite driver, smooth ride, and strict adherence to speed limits.', '2026-08-24 12:19:33.866805', 5, 5, 5, 5, 1, 2, 22),
  (10, 5, 'Comfortable taxi ride, clean vehicle, excellent safety protocol.', '2026-08-24 12:19:33.934012', 5, 5, 5, 5, 2, 2, 23);

-- Table structure for `tbl_sos_alert`
DROP TABLE IF EXISTS `tbl_sos_alert`;
CREATE TABLE `tbl_sos_alert` (
  `sos_id` int(11) NOT NULL AUTO_INCREMENT,
  `alert_uuid` char(32) NOT NULL,
  `location` varchar(100) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `status` varchar(15) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  `location_name` varchar(255) NOT NULL,
  `admin_notes` longtext DEFAULT NULL,
  `dispatched_services` varchar(255) NOT NULL,
  `resolved_at` datetime(6) DEFAULT NULL,
  `driver_id` int(11) DEFAULT NULL,
  `passenger_id` bigint(20) NOT NULL,
  `trip_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`sos_id`),
  UNIQUE KEY `alert_uuid` (`alert_uuid`),
  KEY `tbl_sos_alert_driver_id_09472c68_fk_tbl_driver_driver_id` (`driver_id`),
  KEY `tbl_sos_alert_passenger_id_7ac95545_fk_tbl_user_id` (`passenger_id`),
  KEY `tbl_sos_alert_trip_id_166aeec3_fk_tbl_trip_trip_id` (`trip_id`),
  CONSTRAINT `tbl_sos_alert_driver_id_09472c68_fk_tbl_driver_driver_id` FOREIGN KEY (`driver_id`) REFERENCES `tbl_driver` (`driver_id`),
  CONSTRAINT `tbl_sos_alert_passenger_id_7ac95545_fk_tbl_user_id` FOREIGN KEY (`passenger_id`) REFERENCES `tbl_user` (`id`),
  CONSTRAINT `tbl_sos_alert_trip_id_166aeec3_fk_tbl_trip_trip_id` FOREIGN KEY (`trip_id`) REFERENCES `tbl_trip` (`trip_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_sos_alert`
INSERT INTO `tbl_sos_alert` (`sos_id`, `alert_uuid`, `location`, `timestamp`, `status`, `latitude`, `longitude`, `location_name`, `admin_notes`, `dispatched_services`, `resolved_at`, `driver_id`, `passenger_id`, `trip_id`) VALUES
  (13, 'e8057fa6b2fb4349b35ea3029729dd18', 'Live GPS Distress Location', '2026-08-24 17:15:10.304646', 'Active', '9.684300', '76.685300', 'Test SafeRide Health Check Beacon', 'Passenger 1-Touch Emergency Distress Beacon triggered.', 'Local Police (112) & Emergency Contacts', NULL, NULL, 2, NULL);

-- Table structure for `tbl_trip`
DROP TABLE IF EXISTS `tbl_trip`;
CREATE TABLE `tbl_trip` (
  `trip_id` int(11) NOT NULL AUTO_INCREMENT,
  `trip_uuid` char(32) NOT NULL,
  `start_location` varchar(255) DEFAULT NULL,
  `end_location` varchar(255) DEFAULT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `pickup_location_name` varchar(255) NOT NULL,
  `pickup_latitude` decimal(9,6) NOT NULL,
  `pickup_longitude` decimal(9,6) NOT NULL,
  `drop_location_name` varchar(255) DEFAULT NULL,
  `drop_latitude` decimal(9,6) DEFAULT NULL,
  `drop_longitude` decimal(9,6) DEFAULT NULL,
  `live_latitude` decimal(9,6) NOT NULL,
  `live_longitude` decimal(9,6) NOT NULL,
  `live_updated_at` datetime(6) NOT NULL,
  `share_token` char(32) NOT NULL,
  `driver_id` int(11) NOT NULL,
  `passenger_id` bigint(20) NOT NULL,
  `boarding_address` varchar(255) NOT NULL,
  `boarding_latitude` decimal(9,6) NOT NULL,
  `boarding_longitude` decimal(9,6) NOT NULL,
  `current_latitude` decimal(9,6) NOT NULL,
  `current_longitude` decimal(9,6) NOT NULL,
  `destination_address` varchar(255) DEFAULT NULL,
  `destination_latitude` decimal(9,6) DEFAULT NULL,
  `destination_longitude` decimal(9,6) DEFAULT NULL,
  PRIMARY KEY (`trip_id`),
  UNIQUE KEY `trip_uuid` (`trip_uuid`),
  UNIQUE KEY `share_token` (`share_token`),
  KEY `tbl_trip_driver_id_4041cae1_fk_tbl_driver_driver_id` (`driver_id`),
  KEY `tbl_trip_passenger_id_2d98c078_fk_tbl_user_id` (`passenger_id`),
  CONSTRAINT `tbl_trip_driver_id_4041cae1_fk_tbl_driver_driver_id` FOREIGN KEY (`driver_id`) REFERENCES `tbl_driver` (`driver_id`),
  CONSTRAINT `tbl_trip_passenger_id_2d98c078_fk_tbl_user_id` FOREIGN KEY (`passenger_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_trip`
INSERT INTO `tbl_trip` (`trip_id`, `trip_uuid`, `start_location`, `end_location`, `start_time`, `end_time`, `status`, `pickup_location_name`, `pickup_latitude`, `pickup_longitude`, `drop_location_name`, `drop_latitude`, `drop_longitude`, `live_latitude`, `live_longitude`, `live_updated_at`, `share_token`, `driver_id`, `passenger_id`, `boarding_address`, `boarding_latitude`, `boarding_longitude`, `current_latitude`, `current_longitude`, `destination_address`, `destination_latitude`, `destination_longitude`) VALUES
  (22, '82b8af9eff0f4f07b8345d7cc4dc2ea0', 'Current Boarding Point', 'Pala KSRTC Bus Stand', '2026-08-24 10:19:33.847860', '2026-08-24 10:34:33.847860', 'Completed', 'Current Location', '9.684300', '76.685300', NULL, '9.691200', '76.690400', '9.684300', '76.685300', '2026-08-24 12:19:33.848843', '5c198be2a7964278b668b3efcba8ef6a', 1, 2, 'St. Thomas College Gate, Palai', '9.684300', '76.685300', '9.684300', '76.685300', 'Pala KSRTC Bus Stand', '9.691200', '76.690400'),
  (23, 'f9e305bd9ec6484e881041b9270b67be', 'Current Boarding Point', 'Mar Sleeva Medicity, Palai', '2026-08-23 09:19:33.847860', '2026-08-23 09:49:33.847860', 'Completed', 'Current Location', '9.688000', '76.687000', NULL, '9.712600', '76.685400', '9.684300', '76.685300', '2026-08-24 12:19:33.911657', '4f4d73940a12456cb0ad6ab630ad7a3e', 2, 2, 'Palai Private Bus Stand', '9.688000', '76.687000', '9.684300', '76.685300', 'Mar Sleeva Medicity, Palai', '9.712600', '76.685400'),
  (24, '0cb7ca9da2e84bf3b5b65a4093309187', 'Current Boarding Point', 'St. Joseph\'s College of Engineering, Choondacherry', '2026-08-24 11:39:33.847860', '2026-08-24 12:04:33.847860', 'Completed', 'Current Location', '9.687500', '76.684800', NULL, '9.664000', '76.698000', '9.684300', '76.685300', '2026-08-24 12:19:33.967773', '47c52b98f0194c11826ccb46dddf9630', 1, 2, 'Pala Municipal Town Hall', '9.687500', '76.684800', '9.684300', '76.685300', 'St. Joseph\'s College of Engineering, Choondacherry', '9.664000', '76.698000');

-- Table structure for `tbl_user`
DROP TABLE IF EXISTS `tbl_user`;
CREATE TABLE `tbl_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_user`
INSERT INTO `tbl_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `phone`, `avatar`, `created_at`, `updated_at`) VALUES
  (1, 'pbkdf2_sha256$1500000$NExKjw2djokVVBFV4cepBk$aG7FQtmI7qBTqhS/GqNasGiqQgB0B98h5tsospk5CHg=', '2026-08-24 17:15:08.296631', 1, 'admin', 'SafeRide', 'Administrator', 'admin@saferide.org', 1, 1, '2026-08-23 04:09:05.639717', 'ADMIN', NULL, '', '2026-08-23 04:09:05.640715', '2026-08-24 11:01:44.086137'),
  (2, 'pbkdf2_sha256$1500000$GbXzbde2BX1fhYFaUJz56U$kV2tfAINPD5A0qoM5YMhxtQYcIkONIIy1594QULwYx8=', '2026-08-24 17:16:18.667137', 0, 'vyshnavi', 'Vyshnavi', 'Venu', 'vyshnavi@sjcetpalai.ac.in', 0, 1, '2026-08-23 04:09:09.087679', 'PASSENGER', '+91 9847123456', '', '2026-08-23 04:09:09.088722', '2026-08-24 12:19:30.908744'),
  (3, 'pbkdf2_sha256$1500000$LqYbbCK759PfeVmuNI204T$PESJ7WpPXF74v1YAjBT3T7dzG25wVtFtt12NB79lmVE=', NULL, 0, 'rahul', 'Rahul', 'Kurian', 'rahul.k@gmail.com', 0, 1, '2026-08-23 04:09:12.728602', 'PASSENGER', '+91 9895001122', '', '2026-08-23 04:09:12.729601', '2026-08-24 11:01:46.988777'),
  (4, 'pbkdf2_sha256$1500000$nPFVcWVWeAQoQfu6upKhFl$F/QvWRhUvyWIsMzL1vzzEzw0onrL4jlIidkFj2UmH2Y=', '2026-08-24 17:15:05.866226', 0, 'driver_rajesh', 'Rajesh', 'Kumar', 'driver_rajesh@saferide.org', 0, 1, '2026-08-23 04:09:16.087407', 'DRIVER', '+91 9447182930', '', '2026-08-23 04:09:16.088456', '2026-08-24 12:19:32.271495'),
  (5, 'pbkdf2_sha256$1500000$Y7wkVy4L2GLxoKDuES64a1$jnFG6mZAcW6AuJhMaV2iom4VWjO4uoCAcb1HU5IxdX4=', '2026-08-24 17:14:43.838922', 0, 'driver_anand', 'Anand', 'Joseph', 'driver_anand@saferide.org', 0, 1, '2026-08-23 04:09:19.911832', 'DRIVER', '+91 9847334455', '', '2026-08-23 04:09:19.913869', '2026-08-24 12:19:33.752828'),
  (6, 'pbkdf2_sha256$1500000$brb2FYiWtSy8rvOH5f7Vf6$QdV6GdWFomxBJwXRzS7BRgklFl8GNcvaiVYGmjM22ek=', '2026-08-24 17:14:45.402710', 0, 'driver_suresh', 'Suresh', 'Babu', 'driver_suresh@saferide.org', 0, 1, '2026-08-23 04:09:23.474448', 'DRIVER', '+91 9745112233', '', '2026-08-23 04:09:23.474448', '2026-08-24 11:01:51.492806'),
  (7, 'pbkdf2_sha256$1500000$6PRFReWJH9t2mCrKibFcBs$Lq/+wjUfAI9MS316y/z0j+7/rr7EbcD9pWPCdaLXZV4=', '2026-08-24 17:14:47.242019', 0, 'driver_vinod', 'Vinod', 'Mohan', 'driver_vinod@saferide.org', 0, 1, '2026-08-23 04:09:26.866820', 'DRIVER', '+91 9400223344', '', '2026-08-23 04:09:26.867816', '2026-08-24 11:01:53.030479'),
  (8, 'pbkdf2_sha256$1500000$oFimqWMPwCCPV74BRTEpqY$8zZ0yR6pVxGISl5NdAoSHK7wYH6eol2RZonucWB66io=', '2026-08-24 17:14:50.583605', 0, 'driver_pradeep', 'Pradeep', 'Chandran', 'driver_pradeep@saferide.org', 0, 1, '2026-08-24 05:17:32.674813', 'DRIVER', '+91 9447665544', '', '2026-08-24 05:17:32.675808', '2026-08-24 11:01:54.479704'),
  (9, 'pbkdf2_sha256$1500000$kJlNTxOE5ifRT86Q9Z7lZN$/S7btWVXsFbfnRDFO9OAaoEVZ6gdxGSaYz5APdMUvq4=', '2026-08-24 17:14:52.774216', 0, 'driver_mathew', 'Mathew', 'Varghese', 'driver_mathew@saferide.org', 0, 1, '2026-08-24 05:17:37.166413', 'DRIVER', '+91 9847119988', '', '2026-08-24 05:17:37.166413', '2026-08-24 11:01:56.171868'),
  (10, 'pbkdf2_sha256$1500000$agqyrSDJwt9tnkWl7llvfv$1Jrc06hWqLQm3ve2smpWwXhUy2RwpvT0nwV6Vfty+Cc=', '2026-08-24 17:14:54.996826', 0, 'driver_hari', 'Harikrishnan', 'Nair', 'driver_hari@saferide.org', 0, 1, '2026-08-24 05:17:41.066888', 'DRIVER', '+91 9745887766', '', '2026-08-24 05:17:41.067916', '2026-08-24 11:01:57.899575'),
  (11, 'pbkdf2_sha256$1500000$GJA28sP6KSqf4PryyHEsqR$8GPdiyFDcwu4Iy9WRTRzmT9iNxBFqKDjAEcOV1gYz6c=', '2026-08-24 17:14:56.847854', 0, 'driver_shaji', 'Shaji', 'Thomas', 'driver_shaji@saferide.org', 0, 1, '2026-08-24 05:17:45.089489', 'DRIVER', '+91 9495223311', '', '2026-08-24 05:17:45.090522', '2026-08-24 11:01:59.557127'),
  (12, 'pbkdf2_sha256$1500000$ssD832GhfdKZEYtyOPnq0x$MIy76IXtI6bMTbkWBn7UsBqxqOh1HLmPK3Ni3hMbqRk=', '2026-08-24 17:14:59.042942', 0, 'driver_anoop', 'Anoop', 'Rajan', 'driver_anoop@saferide.org', 0, 1, '2026-08-24 05:17:48.572394', 'DRIVER', '+91 9605443322', '', '2026-08-24 05:17:48.573391', '2026-08-24 11:02:01.193461'),
  (13, 'pbkdf2_sha256$1500000$5MIo90sfowgYLJRQeHQTJW$Ru4NttqmuqCxj2GAYiYETKBW3OCzKlT9zaExapZr0lQ=', '2026-08-24 17:15:00.940375', 0, 'driver_deepak', 'Deepak', 'K. S.', 'driver_deepak@saferide.org', 0, 1, '2026-08-24 05:17:51.026068', 'DRIVER', '+91 9946115500', '', '2026-08-24 05:17:51.026068', '2026-08-24 11:02:02.903963'),
  (14, 'pbkdf2_sha256$1500000$7fyxwmE9Bt8CgagkA7msGs$IOnLqlG3N+oRYPxcM5p48SCv5svrlW8ih6gr+VkhRcQ=', '2026-08-24 10:58:40.339940', 0, 'erferferf', '7874518415', '178872446', 'vyshnavivenu2020@gmail.com', 0, 1, '2026-08-24 10:58:35.301153', 'PASSENGER', '/87/*98568', '', '2026-08-24 10:58:39.804860', '2026-08-24 10:58:39.804860'),
  (15, 'pbkdf2_sha256$1500000$WhLIzvFVCmmONbcHt8IukR$X2/4LOYz+kkwLs0Wq5l1R0vLPKQ3EzMnjvPEh3zAth8=', '2026-08-24 12:15:17.398928', 0, 'vyshnavi_e2e', '', '', 'vyshnavi.e2e@saferide.org', 0, 1, '2026-08-24 11:53:00.238845', 'PASSENGER', '9846012345', '', '2026-08-24 11:53:00.238845', '2026-08-24 12:15:15.843708'),
  (16, 'pbkdf2_sha256$1500000$vupBMEvMIAEVKMVD62wMNx$V1gKs3vsF1ESGRoudOp+tJVqtSEeCsbuz6IpqJS1NmQ=', NULL, 0, 'rajesh_driver_e2e', '', '', 'rajesh.driver@saferide.org', 0, 1, '2026-08-24 11:53:02.089580', 'DRIVER', '9447012345', '', '2026-08-24 11:53:02.090561', '2026-08-24 11:53:03.440197');

-- Table structure for `tbl_user_groups`
DROP TABLE IF EXISTS `tbl_user_groups`;
CREATE TABLE `tbl_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tbl_user_groups_user_id_group_id_96fc015e_uniq` (`user_id`,`group_id`),
  KEY `tbl_user_groups_group_id_d81345eb_fk_auth_group_id` (`group_id`),
  CONSTRAINT `tbl_user_groups_group_id_d81345eb_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `tbl_user_groups_user_id_6dda685a_fk_tbl_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for `tbl_user_user_permissions`
DROP TABLE IF EXISTS `tbl_user_user_permissions`;
CREATE TABLE `tbl_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tbl_user_user_permissions_user_id_permission_id_98f65383_uniq` (`user_id`,`permission_id`),
  KEY `tbl_user_user_permis_permission_id_f2f92266_fk_auth_perm` (`permission_id`),
  CONSTRAINT `tbl_user_user_permis_permission_id_f2f92266_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `tbl_user_user_permissions_user_id_205d273c_fk_tbl_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for `tbl_vehicle_documents`
DROP TABLE IF EXISTS `tbl_vehicle_documents`;
CREATE TABLE `tbl_vehicle_documents` (
  `document_id` int(11) NOT NULL AUTO_INCREMENT,
  `license_doc` varchar(255) NOT NULL,
  `rc_doc` varchar(255) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `license_file` varchar(100) DEFAULT NULL,
  `rc_file` varchar(100) DEFAULT NULL,
  `driver_id` int(11) NOT NULL,
  PRIMARY KEY (`document_id`),
  KEY `tbl_vehicle_documents_driver_id_6a79b144_fk_tbl_driver_driver_id` (`driver_id`),
  CONSTRAINT `tbl_vehicle_documents_driver_id_6a79b144_fk_tbl_driver_driver_id` FOREIGN KEY (`driver_id`) REFERENCES `tbl_driver` (`driver_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_vehicle_documents`
INSERT INTO `tbl_vehicle_documents` (`document_id`, `license_doc`, `rc_doc`, `uploaded_at`, `license_file`, `rc_file`, `driver_id`) VALUES
  (1, '/media/driver_docs/license/lic_KL-05-20180004521.pdf', '/media/vehicle_docs/rc/rc_KL-05-AT-4455.pdf', '2026-08-23 04:09:19.389349', '', '', 1),
  (2, '/media/driver_docs/license/lic_KL-05-20150009812.pdf', '/media/vehicle_docs/rc/rc_KL-05-TX-1024.pdf', '2026-08-23 04:09:23.327728', '', '', 2),
  (3, '/media/driver_docs/license/lic_KL-05-20200003411.pdf', '/media/vehicle_docs/rc/rc_KL-05-CB-8890.pdf', '2026-08-23 04:09:26.691142', '', '', 3),
  (4, '/media/driver_docs/license/lic_KL-05-20240001290.pdf', '/media/vehicle_docs/rc/rc_KL-05-AT-9911.pdf', '2026-08-23 04:09:30.313186', '', '', 4),
  (5, '/media/driver_docs/license/lic_KL-05-20170008821.pdf', '/media/vehicle_docs/rc/rc_KL-05-AT-7788.pdf', '2026-08-24 05:17:37.031038', '', '', 5),
  (6, '/media/driver_docs/license/lic_KL-35-20160007743.pdf', '/media/vehicle_docs/rc/rc_KL-35-TX-4521.pdf', '2026-08-24 05:17:40.946464', '', '', 6),
  (7, '/media/driver_docs/license/lic_KL-05-20190005512.pdf', '/media/vehicle_docs/rc/rc_KL-05-CB-3344.pdf', '2026-08-24 05:17:44.989713', '', '', 7),
  (8, '/media/driver_docs/license/lic_KL-05-20210006678.pdf', '/media/vehicle_docs/rc/rc_KL-05-EV-1205.pdf', '2026-08-24 05:17:48.481969', '', '', 8),
  (9, '/media/driver_docs/license/lic_KL-35-20230009988.pdf', '/media/vehicle_docs/rc/rc_KL-35-AT-6622.pdf', '2026-08-24 05:17:50.958373', '', '', 9),
  (10, '/media/driver_docs/license/lic_KL-07-20140003321.pdf', '/media/vehicle_docs/rc/rc_KL-07-CB-9080.pdf', '2026-08-24 05:17:54.842550', '', '', 10);

SET FOREIGN_KEY_CHECKS=1;
