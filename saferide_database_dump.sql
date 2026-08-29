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
  ('221yifwpy56lhmhvqbceduhzjon4aqu7', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wymaj:T_s1-yFdrjEbN1YT_eto5MJJnU8l7OZCTNaWjIxm4qk', '2026-09-08 08:33:09.837796'),
  ('2cjepgdd321xycm0j4e13kho59xz9byx', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wylmH:nUarNimoes8Q8po_VSzbPaq_9nRXX72LIGOiIMY3rPM', '2026-09-08 07:41:01.865548'),
  ('2cydtlhxht8r9nspuq7ydq38ihlkzwzn', '.eJxVjEEOwiAQRe_C2hBgANGl-56hGWZGqRpISrsy3l2bdKHb_977LzXiupRx7TKPE6uz8urwu2Wkh9QN8B3rrWlqdZmnrDdF77TrobE8L7v7d1Cwl2-NwWUQAuHE0YOjYDLEiCDpGAX5ar2JNgGJNZKACZKnkLMnxycJpN4f8Ng4WA:1wzbq9:yWR16HpVFRbgMaw34j7VcGgzIKsCg2AVDkMwSWlr_7g', '2026-09-10 15:16:29.449289'),
  ('2lofcv9cue42bnpchoy47y0egjrrp5gr', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyAUg:TNHb0NXoF1GatMaE4yFdkrGEHmjoZSokmonN-D8EFpw', '2026-09-06 15:52:22.099990'),
  ('2vrochzp6u9st7j81vmni0gptr88tpuy', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wynKe:yFjJ81oxQTjFW5v9AmgMC-7NpVrteTlq8QdHGjN3sTU', '2026-09-08 09:20:36.290376'),
  ('308v01tbn2d7bpv96drytqofvin96iyt', '.eJxVjDsOwjAQBe_iGlne-E9JzxmsXXuNAyiR4qRC3B0ipYD2zcx7iYTb2tLWeUljEWcxiNPvRpgfPO2g3HG6zTLP07qMJHdFHrTL61z4eTncv4OGvX3rYF0wyoAjb4uruXoCrEEDKU8GFGgyLmpkhxCjHryLmKNFrswGohXvD8RAN04:1wynwr:CKx0R-wO1lutp4EmbLpyO1RWii91nIUzctAgpIRfCLY', '2026-09-08 10:00:05.096785'),
  ('32824wg7lyxmteh883ljicodlhxhqgto', '.eJxVjDsOwjAQBe_iGln-e5eSnjNY6x8OIEeKkwpxd4iUAto3M-_FAm1rC9soS5gyOzPJTr9bpPQofQf5Tv028zT3dZki3xV-0MGvcy7Py-H-HTQa7VtXG9HqqJTCCiICeY_SaGUQjAXlUAFI8iCt1JKE055y8QmMiA6hAnt_AKGcNhM:1wynRt:yODodAhSCRxKL3c_qhGmVdqdnhA9S3NvMLPpXu16BYQ', '2026-09-08 09:28:05.391087'),
  ('35mbm5hzrv0nxi72vyxs3rgv25uhj696', '.eJxVjMsOwiAQRf-FtSHAAAMu3fsNhMdUqgaS0q6M_65NutDtPefcFwtxW2vYBi1hLuzMFDv9binmB7UdlHtst85zb-syJ74r_KCDX3uh5-Vw_w5qHPVbE6BQCVCWZLLWUtjoEXzyohg_GZLOWSAQaVJWWwRE7wmlcLIolVGx9we42DZj:1wyqJv:1riS7ybYppfd5WLRefI_ZjCpKWeer3Xmfyk2erSTkcA', '2026-09-08 12:32:03.771267'),
  ('3j3zy1dlh2lu2v5ddxcdbxnfsty9sbb2', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wySd8:PI350mqNsN7rEs4N6E47tE72vAPtmVLmjTqFwcfg_Zg', '2026-09-07 11:14:18.145975'),
  ('3l365hqez43ilm7lohsa8fvugduaco37', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYg2:oORKmryDPRSEGfc1FxYwGM5YmCn6MdcCJyrQ2pQCc9A', '2026-09-07 17:41:42.654803'),
  ('3sasy4y26o2oc75p4vhonmk5w7j1shy4', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyA6j:uiGBFxAu1_148syIuBIFg9Ubb6bsGwdjfP4NacJHMUM', '2026-09-06 15:27:37.691089'),
  ('41e35yyc05znahvc3vec7ilhje8jk7hu', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wyls5:UgBH1ygmK-Fz3UFqR4kH1FLavZX9y0eGKFdaeNCEgUI', '2026-09-08 07:47:01.842910'),
  ('43xqga4hszrstgp6ajvt1icsssveuegl', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySla:NeOOZ_nNF2A0rloUc0tJ15FoE-oL6dmVLpZ1-DPrOyI', '2026-09-07 11:23:02.700787'),
  ('4ul2zfwubnfjg1bokkm7grh05teimfi0', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wyj8o:k_T-gv9ERBKgbwgtA0TNv7CTkQ0ThFnByFNe4FWT_NQ', '2026-09-08 04:52:06.638701'),
  ('4ul8yqgbl9e5eqxpkirg99c1jdwdfjoo', '.eJxVjDsOwjAQBe_iGlne-E9JzxmsXXuNAyiR4qRC3B0ipYD2zcx7iYTb2tLWeUljEWcxiNPvRpgfPO2g3HG6zTLP07qMJHdFHrTL61z4eTncv4OGvX3rYF0wyoAjb4uruXoCrEEDKU8GFGgyLmpkhxCjHryLmKNFrswGohXvD8RAN04:1wynVv:HX0Ofd1SFiIMFunR2KP_UCgP9tUFVm-ofFUWFKJxlAQ', '2026-09-08 09:32:15.855770'),
  ('4v394iyzbiag8ycwzzbk9u78hkuh1kmj', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyMcx:nxWN7iHaB6xxum8pkARZeQuHDKjqUWakcDzphgkPdL8', '2026-09-07 04:49:43.080869'),
  ('518o1qx6zkgeroj34utnpwa04cav2jyn', '.eJxVjMsOwiAQRf-FtSEMDBRcuvcbyPCSqoGktCvjv2uTLnR7zzn3xTxta_XbyIufEzszZKffLVB85LaDdKd26zz2ti5z4LvCDzr4taf8vBzu30GlUb81oZ2cdmgT5RKtkEGZAqgnaUCAyKiLciWSkmSCgWS1pYJRK8waJAj2_gDNTTcQ:1wy9C5:XN4qCWucoRJwRtf3sodTe-A94VD1pzxoOoHw5J-fujA', '2026-09-06 14:29:05.217100'),
  ('53eahvidrpq72h29ss3nmiqae0nc2v1f', '.eJxVjEEOwiAQRe_C2hBgANGl-56hGWZGqRpISrsy3l2bdKHb_977LzXiupRx7TKPE6uz8urwu2Wkh9QN8B3rrWlqdZmnrDdF77TrobE8L7v7d1Cwl2-NwWUQAuHE0YOjYDLEiCDpGAX5ar2JNgGJNZKACZKnkLMnxycJpN4f8Ng4WA:1wzc3t:ggh5yuepuubMwagtj8x-fkqnVJQzW7mK2sLKwAcKY7I', '2026-09-10 15:30:41.166771'),
  ('56cuef5lggp8fiqi2033cc51yagmy009', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySro:EXybRpb2iRhhIJMXdcCKO2ncGjLxOizZ6QPywRYginI', '2026-09-07 11:29:28.421456'),
  ('5dx0r9l8tjxrezvpacc0y57o1uepk9oy', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wy00k:6pyl6UmMDCdMsAQUWZVbKtTDYCIcqv-FNGc0Wsf_S4c', '2026-09-06 04:40:46.532379'),
  ('5tk6x8zroiw8f61lwrpebvk92jq147d3', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wylmG:asgAi13mOYhwgEN3V45cB_lXDtJnGeDjv-ZqVrvJglE', '2026-09-08 07:41:00.428515'),
  ('60ydfqzhlbo4pz58n1vqcw6ocqvi650a', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYHM:U5wbMUcs2CzkrnitZ6COvqu0xKUcOqnP0cuycpYRf_w', '2026-09-07 17:16:12.018449'),
  ('619o9v7qoell4e6we4b1ctflt89budvj', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyjSs:Zfx16FAJaPaB1tyyQ7oqP7-QisuyB-ukKiWVwBNqdMs', '2026-09-08 05:12:50.930931'),
  ('66w45zqyhuw0kapqydndjepy52fg0id0', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wymQc:C8oPFj6se9MqewSDlKU-kjPLjhyZHfQfkQ0bHuJ5BU8', '2026-09-08 08:22:42.463087'),
  ('6dj2uu7msggpslhvcjezotu5afep0bw9', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyTjk:tK1ZtYAe_ox1TIoTBLusaCMoWK6EVuUSo9yELHTl6qc', '2026-09-07 12:25:12.302661'),
  ('6ejurs8ilkca0ox7wd8ahi3fyu9c4uyj', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wyYg4:8-cg7MQ2Dqj6jmpotgOuWz_kxu48y0Y5gPCD-CgfgK0', '2026-09-07 17:41:44.488633'),
  ('6x5wka9nexlqek9bts7x3g4995j9d5z4', '.eJxVjMsOwiAQRf-FtSHAAAMu3fsNhMdUqgaS0q6M_65NutDtPefcFwtxW2vYBi1hLuzMFDv9binmB7UdlHtst85zb-syJ74r_KCDX3uh5-Vw_w5qHPVbE6BQCVCWZLLWUtjoEXzyohg_GZLOWSAQaVJWWwRE7wmlcLIolVGx9we42DZj:1wyqAE:40wJ3tu0jgh0cg6x63zote0JeT5RwGFZfbFzGBCO2xE', '2026-09-08 12:22:02.077673'),
  ('71ujwo3qaz7qkh6aaz1fts7vgan8kne5', '.eJxVjDsOwjAQBe_iGln-e5eSnjNY6x8OIEeKkwpxd4iUAto3M-_FAm1rC9soS5gyOzPJTr9bpPQofQf5Tv028zT3dZki3xV-0MGvcy7Py-H-HTQa7VtXG9HqqJTCCiICeY_SaGUQjAXlUAFI8iCt1JKE055y8QmMiA6hAnt_AKGcNhM:1wynRu:ssQBD972QoCOBmirMkbfT9lSLSdrBSDcVYOm5H7kSDM', '2026-09-08 09:28:06.718999'),
  ('729tdwi1lxtt893ukrdwc9enbce14nx6', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wyYg3:JC0wAy7LWkk3yAsD6MDz4nK9MC2Y1jcdaOc88XwLwRQ', '2026-09-07 17:41:43.795310'),
  ('74evv651lzh5282w1dcpebhdkcydp29l', '.eJxVjMsOwiAQRf-FtSHAAAMu3fsNhMdUqgaS0q6M_65NutDtPefcFwtxW2vYBi1hLuzMFDv9binmB7UdlHtst85zb-syJ74r_KCDX3uh5-Vw_w5qHPVbE6BQCVCWZLLWUtjoEXzyohg_GZLOWSAQaVJWWwRE7wmlcLIolVGx9we42DZj:1wypcK:QcRiEgRfNrbURGCyf-pd-4D1PZYlfZhatO2pM6zO4Nk', '2026-09-08 11:47:00.646622'),
  ('7cdgjemff4mhr637rmxrumisjq1z104u', '.eJxVjDsOwyAQRO9CHSHWYD4p0_sMCNglOIlAMnYV5e6xJRdJM8W8N_NmPmxr8Vunxc_IrsxadvktY0hPqgfBR6j3xlOr6zJHfij8pJ1PDel1O92_gxJ62dciCwkqKetyIhAIGfdIADgEgxqVzRij1jJaZ0gOxowiS0FR59EpIPb5AhbJODo:1x0Dzz:o9NHl_KECxUnD3bN8dyt-3Ry35-q1iSc6I5SH0pj0zE', '2026-09-12 08:01:11.741567'),
  ('7fh6fqkl1orf1qt787iu31tnpgletty8', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYho:dcDFd63xVyRiTQ9bA_wThH9GVQILu6nh1lGvT-553Bw', '2026-09-07 17:43:32.228791'),
  ('7ln85k2orf7sixr2kyuq5h9l1j4kyyen', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wy9Uh:LWClfDF0w08DQsMgnTZzvXsJOkciJS7EzHzPA6mt2Nk', '2026-09-06 14:48:19.780988'),
  ('7pa2k896wzqroee3evy3i66g3qqlqh2y', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYg3:Y4EBtL976lneAMTfusV6RJf5bikDBGWDZ2FBW0PgchU', '2026-09-07 17:41:43.371863'),
  ('8n8hueo26ws8lcwwcit2t4h2egqdzx0o', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wyj8m:tz28cFlwh3GPOJTbTN0A7UWI72jV3uJvbsIUKi1r6Nk', '2026-09-08 04:52:04.826877'),
  ('98hbv1dyv2sxu94x1ei6kb4giq9svd5w', '.eJxVjEEOwiAQAP_C2RBYpBSP3n0D2WVBqgaS0p6MfzckPeh1ZjJvEXDfSth7WsPC4iJmJ06_kDA-Ux2GH1jvTcZWt3UhORJ52C5vjdPrerR_g4K9jK_niZQ1FnLEqMHniQwSw-zAEJ_Z6QQKY8qYNRmDTAq9ZZ-ZdPIgPl8o-zlK:1wynyx:Ei8hNdjXXZb7WeRaxRQDB4GWjws4AiHaqmJt4rQ4lEo', '2026-09-08 10:02:15.791221'),
  ('9gn4fmlc3wy50grupkpsfj3kyacknot0', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyALL:GNZiCPPSLkruPUnNYRDaeYsdurI905KjyRifpHRP12k', '2026-09-06 15:42:43.196797'),
  ('9m8ejpjkvdkservdvgjag4pm9yeid4yu', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wy9b7:ufiI3GjJ9pyA7iwS9ikx5dQCx4DoxtAI704_GjJKFbo', '2026-09-06 14:54:57.330718'),
  ('9p3crqzoizqpme7ssa7hwy8n5vpgglsc', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wyYg5:E5HXcSYjDFdulAP1sjCtq45O8mW0RTPI_-MVAgM5gKE', '2026-09-07 17:41:45.420389'),
  ('9rp4tln4enmxb7xkajpk73lu9lzttzon', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wxzry:f4ws0tQC-rr29Wm-WL3k-kQrtT6QrV86z0oeiSSEdQE', '2026-09-06 04:31:42.071054'),
  ('abpzna043fwu3qhd1ddgglquyr2x4ka1', '.eJxVjEsOAiEQBe_C2hBgaD4u3XsGQjeNjJohmc_KeHedZBa6fVX1XiLlbW1pW3hOYxFnEbw4_Y6Y6cHTTso9T7cuqU_rPKLcFXnQRV574eflcP8OWl7atx7CwNG6SsSqKGeAciRgAFQ-hBqDQ4w6gi5IvoLTGcgoCwaDYhuNeH8ADeg3wA:1x0Du3:pnZPeygwyxucm5KtXNZOkBlY_hQQzIeTdRaJbFLveMk', '2026-09-12 07:55:03.174481'),
  ('afmitdviimb3yuuvnpe6ngzqv7ypi5c7', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyABj:Q1exz5pp9kpvPcXWtT0zmPJlzVypNyl6ykehlq3w2VU', '2026-09-06 15:32:47.192494'),
  ('at1n3pbdqt8fer9jh2jfhqtirygipqr9', '.eJxVjDsOwjAQBe_iGln-e5eSnjNY6x8OIEeKkwpxd4iUAto3M-_FAm1rC9soS5gyOzPJTr9bpPQofQf5Tv028zT3dZki3xV-0MGvcy7Py-H-HTQa7VtXG9HqqJTCCiICeY_SaGUQjAXlUAFI8iCt1JKE055y8QmMiA6hAnt_AKGcNhM:1wynXO:WnFSCyjdDZOQalsqz7fFkCBkxzIp2p1ukbf7DNC2Jvw', '2026-09-08 09:33:46.987727'),
  ('bpjml9zfr9vt504sp0kqdfssiz4o8wcr', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyA10:0XNShwHMajARMk16qRt8uj_PqS62ixcv84ipp_sMRMI', '2026-09-06 15:21:42.066173'),
  ('bx8cdge3lv5ynn9lm2s3pv63wy8btml3', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYg3:Y4EBtL976lneAMTfusV6RJf5bikDBGWDZ2FBW0PgchU', '2026-09-07 17:41:43.088312'),
  ('c5or1dh4jgkebik078qghzsufjllfd8t', '.eJxVjMsOwiAQRf-FtSHAAAMu3fsNhMdUqgaS0q6M_65NutDtPefcFwtxW2vYBi1hLuzMFDv9binmB7UdlHtst85zb-syJ74r_KCDX3uh5-Vw_w5qHPVbE6BQCVCWZLLWUtjoEXzyohg_GZLOWSAQaVJWWwRE7wmlcLIolVGx9we42DZj:1wypCY:MdXZHzzRgnHrlE2121ge5j9TM-nuVwCLnQ8XEPt30J0', '2026-09-08 11:20:22.514496'),
  ('c776lbs55jfql4h1xzk5ug3v2bf6pl5l', '.eJxVjEEOgjAQRe_StWnoMIXi0r1nINOZqaCmTSisjHdXEha6_e-9_zIjbes0blWXcRZzNs6b0-8YiR-adyJ3yrdiueR1maPdFXvQaq9F9Hk53L-Dier0rX3LbZKkDabOcWi9bzpkDUEgpAQUgbFjB8712KToMYLIgD3BAKgUzPsDDLY4Ag:1wyjXt:itPbaE32FZVKvNkppQjnC7Ey5X-GWQSX3C-DU2IF-pc', '2026-09-08 05:18:01.873672'),
  ('cb8bay9zwcpns6mpcrwtg5dyi9io209q', '.eJxVjMsOwiAQRf-FtSHAAAMu3fsNhMdUqgaS0q6M_65NutDtPefcFwtxW2vYBi1hLuzMFDv9binmB7UdlHtst85zb-syJ74r_KCDX3uh5-Vw_w5qHPVbE6BQCVCWZLLWUtjoEXzyohg_GZLOWSAQaVJWWwRE7wmlcLIolVGx9we42DZj:1x0Dub:Y2ZdUpdbsA9DJqeGDvkBLPzHkF3JoHUVz-8MsuzoDq8', '2026-09-12 07:55:37.509425'),
  ('cc4uwsu3f4tceniuk7teeqo9gvcrvfp9', '.eJxVjEEOwiAQRe_C2hBgANGl-56hGWZGqRpISrsy3l2bdKHb_977LzXiupRx7TKPE6uz8urwu2Wkh9QN8B3rrWlqdZmnrDdF77TrobE8L7v7d1Cwl2-NwWUQAuHE0YOjYDLEiCDpGAX5ar2JNgGJNZKACZKnkLMnxycJpN4f8Ng4WA:1wzbq0:MA12AHqytAT46OzwOG_YNNIQO2ROkS7L1ZcYT7GvplM', '2026-09-10 15:16:20.705267'),
  ('cqfqmqu0pot9rbc288q614opgdgvn2gc', '.eJxVjDEOwjAMRe-SGUVNGsc2IztnqOwkkAJqpaadEHdHlTrA-t97_20G2dY6bK0sw5jN2Tgwp99RJT3LtJP8kOk-2zRP6zKq3RV70Gavcy6vy-H-HVRpda87ZiUFvjEIxtxTQIrUKyfB0BfQCE7Ud4F89glScowsqkgQMZP5fAH4JTef:1wyjjZ:bzX5yuncYt8_pnPmxiexQFWNKQmoMCZwfx4M8xAa5es', '2026-09-08 05:30:05.790318'),
  ('czs8le79obqx2zq3yuqv9if2628tqzdd', '.eJxVjMsOwiAQRf-FtSEgMIBL9_0GMsNDqoYmpV0Z_11JutDVTe45OS8WcN9q2Htew5zYhUnDTr8nYXzkNki6Y7stPC5tW2fiQ-EH7XxaUn5eD_cvULHX0RUoidB9B5TRVhRZkvZgfSFvz5GScqDIIhalpXcAUpZitNcCrHHA3h_34zci:1wyTEx:0Y3NBPNlR5DgsWfCUcn7WbBMng4002ZbxS9lXI3Stxw', '2026-09-07 11:53:23.279229'),
  ('dec5mjl54swoigfs6d1p3egbvffcb8zm', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYg2:oORKmryDPRSEGfc1FxYwGM5YmCn6MdcCJyrQ2pQCc9A', '2026-09-07 17:41:42.888061'),
  ('dfcm9ixea7p3c6fygqz0rubhg1id8n27', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wynDJ:A-ppTj5EKUbzLTxL_Nk6Grs_iM9I1e5BQGrePmmUER8', '2026-09-08 09:13:01.018293'),
  ('dmt9ocgz48boglu68cnls9m97wsacbkl', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wymh1:1__YQQDddup3OiLEh8RC8lZbZa_4O6QgzEZf0FP3_9Y', '2026-09-08 08:39:39.061490'),
  ('drzonki1pnbb64z4m8skgx0f34ao45xm', '.eJxVjDsOwjAQBe_iGln4x7KU9JzBWu86OIBsKU4qxN1JpBTQvpl5bxVpmUtcep7iKOqiTFCH3zERP3PdiDyo3pvmVudpTHpT9E67vjXJr-vu_h0U6mWtBzAZHUO2ICIeBuOctyGRAyvkDZMTQIsYfGZAMIboZJlXchbCo_p8AQpkOAg:1wyTMs:fCahUvqCadTdWxc7Tyl7N52rp5N_vM6ZcpFtieCOp0c', '2026-09-07 12:01:34.428591'),
  ('dvi9beb2x1mj1cw6jywrqt22toudb0l1', '.eJxVjDsOwjAQBe_iGlne-E9JzxmsXXuNAyiR4qRC3B0ipYD2zcx7iYTb2tLWeUljEWcxiNPvRpgfPO2g3HG6zTLP07qMJHdFHrTL61z4eTncv4OGvX3rYF0wyoAjb4uruXoCrEEDKU8GFGgyLmpkhxCjHryLmKNFrswGohXvD8RAN04:1wyny5:QeTqwylTWhfOorFIMCD653lRoJk4SGJb6RwlmxSo7bE', '2026-09-08 10:01:21.800725'),
  ('e013g4q2dwrixenqvx4gyu89ul2gm89g', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wxzyy:QDgAydsXkzHGYaZORh9UBFj__DevZECRq1FhezF1H_k', '2026-09-06 04:38:56.726232'),
  ('e4hv1h000l9qswytmj1rfx74q2kq0lzy', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wyYg5:E5HXcSYjDFdulAP1sjCtq45O8mW0RTPI_-MVAgM5gKE', '2026-09-07 17:41:45.573647'),
  ('ehaj6p60u7lp3r1unrpttitkjku2hqik', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wylrT:3_FL-CmDYmnXdA5WfWstlTIeLGS7L4FZ-8_cCZ0-y9Q', '2026-09-08 07:46:23.652887'),
  ('er6c6mtqwodi19lckad4uiy9dtmu19ps', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wxziG:DLV9apzT1l4rbs4NNO7NWOznBoJSdp0dn--FsmhFYdk', '2026-09-06 04:21:40.621555'),
  ('ev3uu7chknolbw7dq82lwpsk05vwt3ya', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wymU5:Jhjq-F1wp-ex9EseNuFRIxSLQxVRTlghbCGDkH_0ggg', '2026-09-08 08:26:17.868999'),
  ('ez83ubb3thsbpjnrp1arr0kvht9aubid', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wyYg5:E5HXcSYjDFdulAP1sjCtq45O8mW0RTPI_-MVAgM5gKE', '2026-09-07 17:41:45.040156'),
  ('g5jfh1io0qturtbz00l54mzxnjwu2puh', '.eJxVjEEOwiAQRe_C2hBgANGl-56hGWZGqRpISrsy3l2bdKHb_977LzXiupRx7TKPE6uz8urwu2Wkh9QN8B3rrWlqdZmnrDdF77TrobE8L7v7d1Cwl2-NwWUQAuHE0YOjYDLEiCDpGAX5ar2JNgGJNZKACZKnkLMnxycJpN4f8Ng4WA:1wzbqC:gr1nxNfm_egpBDqnxYOObSHTWQBUG0NAjZNBp5lqXus', '2026-09-10 15:16:32.567843'),
  ('g7resse7rywicxapb7qhf0r5ajvccic5', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wyYg4:TN3crImNXZiyjPUylxQvkvkomejGzOSyvEFPsz1Ik-0', '2026-09-07 17:41:44.310133'),
  ('gefjgwqmqn747l4qohzs88bnyukcbuiy', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wyYg3:JC0wAy7LWkk3yAsD6MDz4nK9MC2Y1jcdaOc88XwLwRQ', '2026-09-07 17:41:43.974243'),
  ('gf482ke5y6h75lgtwogfjvxobyo7pbrk', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyMcv:2PNJQNRR7zbS-CRoUYFIN_VJZ3tIsjf0IxdKW0-bsQ0', '2026-09-07 04:49:41.707938'),
  ('gn4t2rmf17xwogzeh4xys1zh25vh4omd', '.eJxVjEsOAiEQBe_C2hAahEaX7j3DpOkGZ9RAMp-V8e5KMgvdvqp6LzXQto7DtuR5mESdFXh1-B0T8SPXTuRO9dY0t7rOU9Jd0Ttd9LVJfl529-9gpGXsdaYi0SUI4BP4gM7bgGyPtmAxX0CFPRtgK8DmlBJipBBRnCkCFtX7Awv9N_s:1wyjRd:J5M8poaXCAipvp62AKe_Gogf06AFhIubg7-WBgdepqE', '2026-09-08 05:11:33.914903'),
  ('gp6nf6yc5jevewy06b9hna90wzabtpmd', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYiD:K4aCfF3zt-uuRC5np00lFJHCcgkuGCmRTd6cezfaYIY', '2026-09-07 17:43:57.667458'),
  ('gqsvn720qpu086vm60xerz0vcnwtfrw8', '.eJxVjMsOwiAQRf-FtSHAAAMu3fsNhMdUqgaS0q6M_65NutDtPefcFwtxW2vYBi1hLuzMFDv9binmB7UdlHtst85zb-syJ74r_KCDX3uh5-Vw_w5qHPVbE6BQCVCWZLLWUtjoEXzyohg_GZLOWSAQaVJWWwRE7wmlcLIolVGx9we42DZj:1x0Dut:61NCjPqCQYM_q1wJdYnh9FjIzv-LJcKVUui_xmL6Y_A', '2026-09-12 07:55:55.169777'),
  ('gtv9i6jeky2vi2sald6755mkycv2oqol', '.eJxVjEEOwiAQRe_C2hAoOBSX7nsGMjCDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwk7gIfRan3zFienDdCd2x3ppMra7LHOWuyIN2OTXi5_Vw_w4K9vKtGZ1lZJcwWoyULAMoyh5M1jCMNCpvGCMo41kDeIvJgVacjdXRDCzeHzcIOJM:1wyYhU:0MwMAYSs-qobyQ4b44tvnb-lT18AD-n-vZ8YB8T2VlA', '2026-09-07 17:43:12.591593'),
  ('gwfzh760lbo384h9e78s8ymald5c7k2d', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyjKX:EXVKw_glCTyRpGAvfWtgLfvxp5qwraRon80gfrU13TU', '2026-09-08 05:04:13.201233'),
  ('h02zdkv28uj2c5xxc61np6tajjr8fyhf', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wynC1:o5ARsIxQQm9rPFsn6hnG-SySUjrgSDBE8Xvjfc8MkeI', '2026-09-08 09:11:41.686228'),
  ('h50j4oa7fwrrlqsp7mhzhpe2mdlj2yg7', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wymeH:Z2Ln1AJCjtBMmN-htRUagY3CpAqXNgUCxZ0ci7XYjvs', '2026-09-08 08:36:49.743627'),
  ('hazhvvwhzah1xune0rfuvaujfc952c2r', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyN03:AGLYh5kLV6-P74rVywgE6u4emiAAwKUWbw83us8iJJ4', '2026-09-07 05:13:35.991653'),
  ('hbkl7esfwqficlecehuddeciny6yfp6a', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9vD:-kxkDOpHL0SSenicoXMjfX1sjqxokPw0pwwLXS9cEQM', '2026-09-06 15:15:43.621277'),
  ('i0rkhttrltu57bym3pbrycc0crqd3rdh', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wyYg4:8-cg7MQ2Dqj6jmpotgOuWz_kxu48y0Y5gPCD-CgfgK0', '2026-09-07 17:41:44.872320'),
  ('iaxvo6h28h1ztg2397rn3r7vwl6hzim6', '.eJxVjMEKwyAQRP_FcxHNatQee883yK4uNW1RiMmp9N-bQA4tzGnem3mLiNta4tZ5iXMWV6GtuPyWhOnJ9SD5gfXeZGp1XWaShyJP2uXUMr9up_t3ULCXfU1KccpKg7dGmz0-aeLBuJHAGGZwHKxCAwrC6CgDBPQ8eNaKNLogPl_iADcF:1wyjxm:prr92LyOT3bILF7ebcQsLaOL5vlXqrDWJemvK9jfRSc', '2026-09-08 05:44:46.103586'),
  ('iqvvv3uwe5iepn7gtd6qzaer7t4map28', '.eJxVjDsOwjAQBe_iGlne-E9JzxmsXXuNAyiR4qRC3B0ipYD2zcx7iYTb2tLWeUljEWcxiNPvRpgfPO2g3HG6zTLP07qMJHdFHrTL61z4eTncv4OGvX3rYF0wyoAjb4uruXoCrEEDKU8GFGgyLmpkhxCjHryLmKNFrswGohXvD8RAN04:1wynQ1:wLIARSg7D2OuAT24lSytdu5CH95Zs8SfwsQWqYMYSmM', '2026-09-08 09:26:09.680094'),
  ('ivw2lmya0xb1flxbmkz0is0paqz7ddv2', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wympb:NmYBQCtDpbrWe3M8VbQ--toF67-BoonHDFbJUcQe9cA', '2026-09-08 08:48:31.587707'),
  ('izkrlq5cqlwch5xr8xs9594a9fcsqx7j', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyTez:rEShX6TDrZi6YrJG2pyC8vjDTCoRvG9jIZliFMUjWlQ', '2026-09-07 12:20:17.786114'),
  ('j2kylszwkghr3u9xguhcum114z6c4gmh', '.eJxVjEEOwiAQRe_C2hAopQwu3XsGMsOAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnEW4MTpdySMj1R3wnestyZjq-syk9wVedAur43T83K4fwcFe_nWaBWDp4GST94obbWB6DRCzkM0E7JFYMzReVLKgdbEJk5EefQwGp3F-wMYPzhu:1wynyY:eEiVXdCxQHGUrXge3JB98P1T9zm4ZI4tEsTS0x5UAeQ', '2026-09-08 10:01:50.310185'),
  ('jbamtmavj3o55w6cpblag2y4qe65wejg', '.eJxVjDEOwjAMRe-SGUVOU5yUkZ0zVHZsSAElUtNOiLtDpQ6w_vfef5mR1iWPa9N5nMScTAzm8DsypYeWjcidyq3aVMsyT2w3xe602UsVfZ539-8gU8vfWtl5Qb32ikdAAUcDDiKKEX2XOEVgD5Q0MoBnCSocOocD9kDcSzLvDyUjOL0:1wynvs:pGrkOrDMxj9fPs-XYAdRIPilwDKGgo--WRTJ-OOHcqg', '2026-09-08 09:59:04.200937'),
  ('jteq5x8spd9dagk1enr2f5a6gk7cggsu', '.eJxVjEEOwiAQRe_C2hBgANGl-56hGWZGqRpISrsy3l2bdKHb_977LzXiupRx7TKPE6uz8urwu2Wkh9QN8B3rrWlqdZmnrDdF77TrobE8L7v7d1Cwl2-NwWUQAuHE0YOjYDLEiCDpGAX5ar2JNgGJNZKACZKnkLMnxycJpN4f8Ng4WA:1wzbq5:i5iW8wpPhBaLAqurUc_XsF6rDgey3GJTXZ7ELuW2718', '2026-09-10 15:16:25.845619'),
  ('k36tetd2ubxhdjzorpc0895j3x9rf5b0', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySlK:QWOf837xWXUOtUpPZSYRxbyc9AthhqrkAVeV3bKTs8A', '2026-09-07 11:22:46.581981'),
  ('kawu67ffymxbzz813ghuy7nxnnxo1hvu', '.eJxVjEEOwiAQAP_C2RC2BaQevfsGssuyUjU0Ke3J-HdD0oNeZybzVhH3rcS95TXOrC4KnDr9QsL0zLUbfmC9LzotdVtn0j3Rh236tnB-XY_2b1Cwlf4d2YRMYn1OQ-DBTwDi0FnwJOCmsxEAsiOYIZhEgCiSXHCJOAjbSX2-_t84KQ:1wykCH:xW4Cp0qQ9GZS8H2wONEZdN0kqqvUwGItsDreyeAgvcM', '2026-09-08 05:59:45.963433'),
  ('kepf622d6k7bhnx5oxlvjhb47tgjjc3u', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySfW:J08bNGTDM4KvGcdJvtw9LvnYhmFEJ30Us3uSvgYmbJE', '2026-09-07 11:16:46.643680'),
  ('kjog9dfohk3vj6n5w1y38bsu04zhfnga', '.eJxVjMsOwiAQRf-FtSHAAAMu3fsNhMdUqgaS0q6M_65NutDtPefcFwtxW2vYBi1hLuzMFDv9binmB7UdlHtst85zb-syJ74r_KCDX3uh5-Vw_w5qHPVbE6BQCVCWZLLWUtjoEXzyohg_GZLOWSAQaVJWWwRE7wmlcLIolVGx9we42DZj:1wzc6c:Aw1inPnjBEtEJnxJlmyGZSft3LVtBQOTnFrQYNZbQ00', '2026-09-10 15:33:30.990403'),
  ('kxorafrlhkn3p7ptdgfemp2xneuljb5x', '.eJxVjDsOwjAQBe_iGln-rL0OJT1nsNY_HEC2FCcV4u4QKQW0b2bei3na1uq3kRc_J3Zm0rDT7xgoPnLbSbpTu3Uee1uXOfBd4Qcd_NpTfl4O9--g0qjfWhOAJuGUpmKLFVkqIGUC5hKn6GRGTQpL0CKQBeuiEkYYRFABsODE3h_7tTdt:1wyjg3:rDB6IyMNA0Z5mfBsucPKclb03V1pR-olbPhEVj2fOCA', '2026-09-08 05:26:27.115880'),
  ('lio589z6o4aae6m17j7017dozphqrzq7', '.eJxVjDsOwjAQBe_iGln-rgMlfc5grXdtHECOFCcV4u4QKQW0b2beS0Tc1hq3npc4sbgIo8Tpd0xIj9x2wndst1nS3NZlSnJX5EG7HGfOz-vh_h1U7PVbpwKGvDPgyxCg6LNTEJC0IzbWOQAmQq3RBo8ZtMrWsA3FslYYeGDx_gD0MDfE:1wympz:fY-q5dGKPhSqT6_Z3XwjyrfgxA_5V83h7Q0EpU7BKc4', '2026-09-08 08:48:55.060854'),
  ('lk7w3ezejmafbcg7kc6at0vomhpoh5ik', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyA6H:2qcp5OQwmzSM1o0rhvRm4jmguDHYDRHzfTOEXvJ-ThQ', '2026-09-06 15:27:09.201631'),
  ('loz3op5d2utkxajkvwso0kkbx4uxl8d9', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyjKS:ZtLdi1EzeXhT1fE3ymS5IppgfRhlQUzyDWp4lFyulyw', '2026-09-08 05:04:08.954649'),
  ('lwuu8uotc9n3r8ezjq34yv2yv2hab8sp', '.eJxVjMsOwiAQRf-FtSEyvF267zeQAQapGkhKuzL-uzbpQrf3nHNfLOC21rANWsKc2YUJzU6_Y8T0oLaTfMd26zz1ti5z5LvCDzr41DM9r4f7d1Bx1G_thcJSIpC3kUQCEWW22YIv3kRTVHLJWUlgM2rSxQChULbAGWTyThr2_gAjBThN:1wykI5:lvT8kjOY2K9SVxkxmqVYL6sggQZgRT3UVbHxGdHfBfM', '2026-09-08 06:05:45.408883'),
  ('lxkp3ck23wwovar7qry3lxj2h4gc9qom', '.eJxVjDsOwjAQBe_iGlne-E9JzxmsXXuNAyiR4qRC3B0ipYD2zcx7iYTb2tLWeUljEWcxiNPvRpgfPO2g3HG6zTLP07qMJHdFHrTL61z4eTncv4OGvX3rYF0wyoAjb4uruXoCrEEDKU8GFGgyLmpkhxCjHryLmKNFrswGohXvD8RAN04:1wynzR:OUf2q1qwi8Pxbzvt4BrJ6RwhXomyvONlPox7qufGeP0', '2026-09-08 10:02:45.020044'),
  ('lyg3zfkdoxnoy1z0f97q3ykf6zkzp1bs', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9lU:vci5YnQfyMX6eWEUlBjxrGr1MRNLeUdkjNgekfJp9_k', '2026-09-06 15:05:40.040081'),
  ('mkt933dpi9kti29lv3j1k2ivyit7p90v', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wyYg5:E5HXcSYjDFdulAP1sjCtq45O8mW0RTPI_-MVAgM5gKE', '2026-09-07 17:41:45.240510'),
  ('mncxzx90l6b6eugo0hwo7nw04shavie2', '.eJxVjDsOwjAQBe_iGln-e5eSnjNY6x8OIEeKkwpxd4iUAto3M-_FAm1rC9soS5gyOzPJTr9bpPQofQf5Tv028zT3dZki3xV-0MGvcy7Py-H-HTQa7VtXG9HqqJTCCiICeY_SaGUQjAXlUAFI8iCt1JKE055y8QmMiA6hAnt_AKGcNhM:1wynYa:Ou9jme8tF6wgiWnpCnLKRGm4gV0Ff9ujMfbDkwAV9SY', '2026-09-08 09:35:00.866085'),
  ('nq8seqc43sbnep7zlh4a4tb35ykx21rg', '.eJxVjE0OwiAYRO_C2pBC5c-l-56BwDcgVUOT0q6Md1eSLnQzi3lv5sV82Lfi95ZWP4NdmDDs9FvGQI9UO8E91NvCaanbOkfeFX7QxqcF6Xk93L-DElrp6xyVdAKj1ePZBgUSJgHOqSE7GQ2y_oaQGSBHCtoqIiOiNUkPOhN7fwAhMTjq:1wym3x:M-JiU5q7UcgTOEImy-epBgT4awylC_UzUspCEZndn3s', '2026-09-08 07:59:17.521658'),
  ('nqopyy90hd4uzosh1pefxwywu9p6q1yg', '.eJxVjMsOwiAUBf-FtSHQC6W4dO83NPeBUjWQlHZl_HfbpAvdzsw5bzXiuuRxbWkeJ1FnZb06_UJCfqayG3lguVfNtSzzRHpP9GGbvlZJr8vR_h1kbHlbU5AbJrY2sjNM3hgTQSBxcJF6EtiAFcABvWfbB-g4GrTAAxnXAanPFxTON9U:1wykFj:gsfuzRAp6A2ch5IAdjnyI1KYHOhJHPxXlklFSVzSK2A', '2026-09-08 06:03:19.937884'),
  ('o1xijtwojng8znzsbk1o7wki3n1js718', '.eJxVjDsOwjAQBe_iGlne-E9JzxmsXXuNAyiR4qRC3B0ipYD2zcx7iYTb2tLWeUljEWcxiNPvRpgfPO2g3HG6zTLP07qMJHdFHrTL61z4eTncv4OGvX3rYF0wyoAjb4uruXoCrEEDKU8GFGgyLmpkhxCjHryLmKNFrswGohXvD8RAN04:1wynVp:4NDD5tKb4khrpW3cg7uQ7ijBLeIe6SJAlQLTIKDSonU', '2026-09-08 09:32:09.032054'),
  ('oaxgpk9fkksmb6skizjic5q3jcew2s6q', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wyYg5:E5HXcSYjDFdulAP1sjCtq45O8mW0RTPI_-MVAgM5gKE', '2026-09-07 17:41:45.722094'),
  ('obzmx18jcao7q5elbw9z28729eznt4gj', '.eJxVjMsOwiAQRf-FtSEMDBRcuvcbyPCSqoGktCvjv2uTLnR7zzn3xTxta_XbyIufEzszZKffLVB85LaDdKd26zz2ti5z4LvCDzr4taf8vBzu30GlUb81oZ2cdmgT5RKtkEGZAqgnaUCAyKiLciWSkmSCgWS1pYJRK8waJAj2_gDNTTcQ:1wyAFc:qtoBC7-TmnnOp-ZTH8M7spoQz49XWOdJQzng8xZ5ahA', '2026-09-06 15:36:48.732936'),
  ('okjb6q6v2qomlo9to64ago03apnkpmoq', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9ut:rUbBH9iA1R1OkwCmH_4U8_OXTRPHOXp7ZHNBDsdK7gE', '2026-09-06 15:15:23.998029'),
  ('p19g8di6h54yq4c58k7rt338upxfgr0m', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYg3:Y4EBtL976lneAMTfusV6RJf5bikDBGWDZ2FBW0PgchU', '2026-09-07 17:41:43.243802'),
  ('p3ju6c1y43sk8z1gywjuhsk9cmyk7me4', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wynCE:7ScHoHwQdT2HrVN--n1Op3BNM2cMsb9c2oJFcdogEjM', '2026-09-08 09:11:54.208637'),
  ('p50ztexosm7wazmbudkdzc4h6d6ei7du', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wyYg4:TN3crImNXZiyjPUylxQvkvkomejGzOSyvEFPsz1Ik-0', '2026-09-07 17:41:44.128777'),
  ('pgrx18qve2kk5cwrlyjruhftq08ambf0', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySsU:KwK4Yo2HMF9blVOwaHXDERRF92d88PDPaln8X7PXE2M', '2026-09-07 11:30:10.435936'),
  ('pzxqijbko2396x01m6943jni4cxnt7rm', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wyjTz:v1JdA-y05sH_CuhE69YVoM4JwzSIt4myjTWs_AcDQJk', '2026-09-08 05:13:59.084427'),
  ('q3j05pgzovkzbb8z2tcok0urodu0dn80', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyAT0:FYcp77o4sPxw99SHXisQ1yEVKWd_6Hd02WlG8E6GNDc', '2026-09-06 15:50:38.753726'),
  ('qatibajo3srupbra44acubq58li1wq9e', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wymUI:wqunEKFCNgTvfuwpna1EfxoPPx5l-pRkWqh-dFPuaTY', '2026-09-08 08:26:30.833643'),
  ('qhn10haz9g86cqt2o8nb4ijqoiy9eux8', '.eJxVjMsOgjAQRf-la9NAYdrRpXu-gcwLixpIKKyM_64kLHR7zzn35Xra1txvxZZ-VHdxNbjT78gkD5t2oneabrOXeVqXkf2u-IMW381qz-vh_h1kKvlby3kwkRawaRKkRttQMZtRFGyFq4gYIWkiQSREZB1CAgCtjUWDBff-ABtHOK8:1wyk8W:C6uAIDBBwaTdQ2dHuRaL-eAML31AAQNEdqBz2t53Za4', '2026-09-08 05:55:52.662832'),
  ('qjybvro9r4128aqo6qfdd2zutd0ywejs', '.eJxVjMsOwiAQRf-FtSEMDBRcuvcbyPCSqoGktCvjv2uTLnR7zzn3xTxta_XbyIufEzszZKffLVB85LaDdKd26zz2ti5z4LvCDzr4taf8vBzu30GlUb81oZ2cdmgT5RKtkEGZAqgnaUCAyKiLciWSkmSCgWS1pYJRK8waJAj2_gDNTTcQ:1wxzoU:XwdXXGWpe4pwyAA4lzLFrniGh2D1dcdVu_XilKpsG3I', '2026-09-06 04:28:06.837610'),
  ('r3zst1bvwggmewhajdkhfw75qg5r11yn', '.eJxVjDsOwyAQRO9CHSGDw2dTpvcZEOxCcBKBZOwq8t0dJBdJM8W8N_Nhzm9rdluLi5uJ3ZgAdvktg8dXLJ3Q05dH5VjLusyBd4WftPGpUnzfT_fvIPuW-zoFJUHQaPV4tV4RChOJANSQQAZDSX9DyESEgIq0VYhGBGuiHnRCth8iYzjs:1wym4R:CoGs4G1RyOKT45CUBkCaLn47SbgqOAiKxSJPYjD1obY', '2026-09-08 07:59:47.717344'),
  ('rkjvndx5f0qleg7yp8zw0vzpf2mrbmnv', '.eJxVjEEOwiAQRe_C2hARhjIu3fcMZGBAqgaS0q6Md7dNutDtf-_9t_C0LsWvPc1-YnEVSpx-t0DxmeoO-EH13mRsdZmnIHdFHrTLsXF63Q7376BQL1udHQZwykVEsBedM9vEZ0oYghu0AeTBabAJQTmrWfGmELIFQ9FqMuLzBeAXN9Q:1x0Drc:QXQOJUGFzee60ookTs_HN5J1Zjb83G22gryIGbhgBDU', '2026-09-12 07:52:32.891384'),
  ('rqih6nqnhife6lp3p50i7w0j47v1h9g7', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9rI:FVbnfwybMh1hYIMoI-5VcAglJSnlMhx5iQHwmrfGnC0', '2026-09-06 15:11:40.280175'),
  ('sggz2e3u5p4fgeko2gpikuvo659i1hm0', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wynDa:KvAy5ZC44rcEIKfm0BK8xiN22YaM6Tx8mP6VCnODDKE', '2026-09-08 09:13:18.934961'),
  ('t0jpfyj6dnz2wg1tc5p6w08apa1tfs9n', '.eJxVjDsOwjAQBe_iGlne-E9JzxmsXXuNAyiR4qRC3B0ipYD2zcx7iYTb2tLWeUljEWcxiNPvRpgfPO2g3HG6zTLP07qMJHdFHrTL61z4eTncv4OGvX3rYF0wyoAjb4uruXoCrEEDKU8GFGgyLmpkhxCjHryLmKNFrswGohXvD8RAN04:1wynz8:JA8jFImq4mfmyMJAWFsQw-2sUP_kyWWVtm1IMGivtIQ', '2026-09-08 10:02:26.669547'),
  ('t14tfa2fwubcn74ygopynma1coenninz', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySek:RxXdQ9VoUCMbbCvX4r_UjKc6WYUJs2YFUL1nUH2HZHE', '2026-09-07 11:15:58.177099'),
  ('t5gcss88petw6tu5bfv5f19xrd5s3xre', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyABl:YNV3vUM0XRn22_p1zirBrEX_09wFQzvMKCsROWsEESU', '2026-09-06 15:32:49.026076'),
  ('t9825qhow33pluxhj05002ga0b8ofnoi', '.eJxVjMsOwiAQRf-FtSEMDBRcuvcbyPCSqoGktCvjv2uTLnR7zzn3xTxta_XbyIufEzszZKffLVB85LaDdKd26zz2ti5z4LvCDzr4taf8vBzu30GlUb81oZ2cdmgT5RKtkEGZAqgnaUCAyKiLciWSkmSCgWS1pYJRK8waJAj2_gDNTTcQ:1wyAF0:mzkAoMzBb6fO3wNC93xTJfv-dK1cSxcxS-yoBQa4dtE', '2026-09-06 15:36:10.420736'),
  ('tgjvosq7v8a7rxgzmh1vha20nxxdodzc', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySiu:4KM928IikNTqy7gqzS2290IMgeLw8fqFR2X9evfJ5yo', '2026-09-07 11:20:16.562687'),
  ('tjuzwuhfk2k30tpa2a9gtu0mbh183diw', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyABm:JH6hZ7OVK5OH6IQtJ4q8jNjxFsFbZOfB-r2v8r3c5Z4', '2026-09-06 15:32:50.658393'),
  ('u23s5k8azkmsssfjqb8d20980y6fk6zh', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wyAL0:LfZb-obZt4Lm0QKSXnCFjT_1LGT5oONs9xMMGfcQ3Z0', '2026-09-06 15:42:22.593628'),
  ('u92t012nmgx60h1f748rj5bny1dpjo6b', '.eJxVjDsOwjAQBe_iGlne-E9JzxmsXXuNAyiR4qRC3B0ipYD2zcx7iYTb2tLWeUljEWcxiNPvRpgfPO2g3HG6zTLP07qMJHdFHrTL61z4eTncv4OGvX3rYF0wyoAjb4uruXoCrEEDKU8GFGgyLmpkhxCjHryLmKNFrswGohXvD8RAN04:1wynXz:7LgGZLt-eUOZj1YLCsvvMi-UnPnpYyd6eRP_5mvFEek', '2026-09-08 09:34:23.613876'),
  ('ua7kivsa7uy9fkkd3tou5c46k3lgf5ng', '.eJxVjMsOwiAQRf-FtSEMDBRcuvcbyPCSqoGktCvjv2uTLnR7zzn3xTxta_XbyIufEzszZKffLVB85LaDdKd26zz2ti5z4LvCDzr4taf8vBzu30GlUb81oZ2cdmgT5RKtkEGZAqgnaUCAyKiLciWSkmSCgWS1pYJRK8waJAj2_gDNTTcQ:1wyAHD:5rmVT1bOLlucE0Ta485d3dRsR4pSru-V6MWELvGscXs', '2026-09-06 15:38:27.528843'),
  ('ufyxoolam0n5finoi3ifsxt3s76wvk7w', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYHR:yY-uAYwrGTvJNSP-wKfDsqx-O_Ym78UBHLNYOi5kIAc', '2026-09-07 17:16:17.506959'),
  ('uicqs56thnxh22pfiqogq455bdc7n1er', '.eJxVjDsOwyAQBe9CHSHwml_K9D4DWlgITiKQjF1FuXuE5CJp38y8N_N47MUfPW1-JXZlUrHL7xgwPlMdhB5Y743HVvdtDXwo_KSdL43S63a6fwcFexk1pNlIocg6oCmarHHOmC0INAhRUEQC6XROYXJJRKt0lppEQFAaSLPPFxtxOJA:1wyjrE:KcKg28G8-89WGI9ALgq9Kn7zTACht_puAvAuqtl4CB4', '2026-09-08 05:38:00.485800'),
  ('up1590xdbm1hwrjsa4o6offpvjkcc1x1', '.eJxVjEEOwiAQRe_C2hAGKKBL9z0DmWFAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERIE6_G2F65LYDvmO7zTLNbV0mkrsiD9rlOHN-Xg_376Bir996MGCQLGOBTGCLHgC94xQCKlW0SZ5cQXfWFCyw8UZbJipWASkXOIn3B-s2OBE:1wxzjV:FmPqt80Q-607Ih5w_LlXb26gAfwen0R-N_73BZkL3L0', '2026-09-06 04:22:57.139573'),
  ('uuo274r1hbd6lkncrxpakt52rmvvzhe3', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wymt1:3ZZJjRYvaXe57lvnUSHyCwbgx7Qf2PiwK5u80_IqxBE', '2026-09-08 08:52:03.799384'),
  ('v02fe23ll5q1qlvwl5x5q65uxokky9hl', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wylrQ:jS9S2iBsvpgLiCOBEf8MUFZze0KwyddoxpI_IXjJhYA', '2026-09-08 07:46:20.777694'),
  ('vbdsyo47ih3yjkbha6ezpgmkt88mbs6q', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy9lV:-PRnr9SIFLzz2nruFDBPzVAcXex_KhnX66MgOL_Z1jo', '2026-09-06 15:05:41.264685'),
  ('vh0e58lmn4izdv4rxlggm2noujrtrfrz', '.eJxVjEEOwiAQRe_C2hBgANGl-56hGWZGqRpISrsy3l2bdKHb_977LzXiupRx7TKPE6uz8urwu2Wkh9QN8B3rrWlqdZmnrDdF77TrobE8L7v7d1Cwl2-NwWUQAuHE0YOjYDLEiCDpGAX5ar2JNgGJNZKACZKnkLMnxycJpN4f8Ng4WA:1wypz7:NymsF0eerGYbrZch_CppMhplK8EPQPWKNBfXIr_6wHA', '2026-09-08 12:10:33.345493'),
  ('vo0ua200fihdujvfi1vpldovounxcane', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wylrW:puyamHAMDqcBpwiuQV5mPLRqa39ZktVPUqasF4TgerI', '2026-09-08 07:46:26.680309'),
  ('vo1ztr1do1go6qqqwoskozg0unjs8w7t', '.eJxVjMsOwiAQRf-FtSFhGF4u3fsNhBlAqoYmpV0Z_12bdKHbe865LxHTtra4jbLEKYuz8E6cfkdK_Ch9J_me-m2WPPd1mUjuijzokNc5l-flcP8OWhrtWydE7ylTtbk4a1QormZ0hKCMJR0YoBpAdsFyCKgr-gIMiqpBzWTE-wMRZzf6:1wynvE:67T_wOkzXb5uvKZR6h-IN4gTx3J3ioMWo51r29o2Xfc', '2026-09-08 09:58:24.532040'),
  ('w1b5su7ekotq3bewlan0zinube8yydpc', '.eJxVjDsOwyAQBe9CHSGD-aZM7zOg3QWCkwgkY1dR7h5bcpG0b2bemwXY1hK2npYwR3Zlll1-NwR6pnqA-IB6b5xaXZcZ-aHwk3Y-tZhet9P9OyjQy14rkkYSoTXa6iyFTxLMAHoYNSA5FFrJaJwe5eh9wpwoI6rdswIok2OfL9n-OAE:1wzc2A:r-SdX5jBwXFwE-ROcGbgA0I3SsY-nLEaYpSrW6tZ1zE', '2026-09-10 15:28:54.115963'),
  ('w9td223ujggind41x7381jleooqj8d6v', '.eJxVjDsOAjEMBe-SGkU4IT9Kes4Q2bHDLqBE2k-FuDustAW0b2beS2VclyGvs0x5ZHVWJ3X43QjLQ9oG-I7t1nXpbZlG0puidzrra2d5Xnb372DAefjW1R05gaco4kqwApASJLbVBqwSBUth8OCMAxNZPFEgwIhiIECkpN4f8vg4PA:1wymXP:KVG0q31NshZyzU8XxGXw0tas3ENvPG-q25LhG96S2ng', '2026-09-08 08:29:43.362074'),
  ('wcywryvgk4p5pu34fa08s0htmu1b1orv', '.eJxVjDsOwjAQBe_iGlne-E9JzxmsXXuNAyiR4qRC3B0ipYD2zcx7iYTb2tLWeUljEWcxiNPvRpgfPO2g3HG6zTLP07qMJHdFHrTL61z4eTncv4OGvX3rYF0wyoAjb4uruXoCrEEDKU8GFGgyLmpkhxCjHryLmKNFrswGohXvD8RAN04:1wynVs:A-WveQxMdKmk4Q6Om3scItrpCLWCWAY52CUD6QPiaGw', '2026-09-08 09:32:12.620675'),
  ('webgmqu0nedohzouybu8n7es4109ncts', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyYg3:Y4EBtL976lneAMTfusV6RJf5bikDBGWDZ2FBW0PgchU', '2026-09-07 17:41:43.517775'),
  ('wkpevw4r6374q6ymj2gq39i2azeiwn6h', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyliz:FuL84LikB3BNLBXQWhYuw69caOrbZ_WAMVhwBEgTmxE', '2026-09-08 07:37:37.127695'),
  ('wsemdcnkgy056wheqohcnnwhsxwmbrez', '.eJxVjDsOwjAQBe_iGln-rRNT0nMGa9fr4ACypTipEHeHSCmgfTPzXiLitpa49bzEmcVZaBCn35EwPXLdCd-x3ppMra7LTHJX5EG7vDbOz8vh_h0U7OVbZ6WM96MBS-hUAjCGErM3CsFNGQNxcBrTYBlShgCoKfjB-HFyFgDF-wP8NDfL:1wyk6j:pW6xWyLchtVLVkBQlC2goeQtm53rtYHJVEBdWQGN2dE', '2026-09-08 05:54:01.886170'),
  ('x845v1axmaoyu6cqelgbonwqm1t0hsj2', '.eJxVjDsOwjAQBe_iGlk2_iWU9DmDtetd4wCypTipEHeHSCmgfTPzXiLCtpa4dV7iTOIitDj9bgjpwXUHdId6azK1ui4zyl2RB-1yasTP6-H-HRTo5VtboJSYbTLsRuWsIq_0WYcADgYgy0GZDD5nlQKgQzSAYAbGnEfPisX7AwPqOTw:1wyN9H:Rq8dHa3RtPMyfu3m5HTDqjr1sZMKKtEjuGWbuWELfVc', '2026-09-07 05:23:07.984569'),
  ('y4l9k23ky1w4o4elmhuzymbkezqxrotc', '.eJxVjDsOwjAQBe_iGln-26Kk5wzW2ruLA8iR4qRC3B0ipYD2zcx7iQzb2vI2aMkTirPQ4vS7FagP6jvAO_TbLOvc12UqclfkQYe8zkjPy-H-HTQY7VsDA1l2zBgK22p19U5Z5BiN8mQDGq2AUlTAkYI3DAZc0rUkLKmwE-8PD8M45Q:1wySf2:DWxwDXJMfgKVOD1OfY1XzOl7mmVIHJAljZv_GCC_seY', '2026-09-07 11:16:16.326653'),
  ('y5004ok0k1mras7le6qtue3ih5a5gdwf', '.eJxVjMsOwiAQRf-FtSFleBRcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnAeL0uyWkB9cd5DvWW5PU6rrMSe6KPGiX15b5eTncv4OCvXxrZZwCoww4sMnbwY-kmJ3NTBw8WcTMwUzZciBQSBp0SG7UgSbLgwPx_gDJ9jer:1wySfq:YuQgVBXZmX-rlofGI8AvWgWFKvj5Thia3KcgtDdXGew', '2026-09-07 11:17:06.129541'),
  ('ydmclhufbwtwspemcmavjej025q3dn6r', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wyA9I:Oxx8dumEB_DmcxuqUpPirY218xxPRrwP1QPfziu7AIM', '2026-09-06 15:30:16.716132'),
  ('yu2nkrbhy59t3g3jl951m605fvzp2qvn', '.eJxVjMsOwiAQRf-FtSEwM0Bx6d5vaIZHpWogKe3K-O_apAvd3nPOfYmRt7WMW8_LOCdxFiBOv1vg-Mh1B-nO9dZkbHVd5iB3RR60y2tL-Xk53L-Dwr18a8wEbAc0SgdLiDQZSn7yEIDRWAZlomZCctZpOxE7jR6i86CCzmoQ7w-tHDZD:1wy88y:X1JiT2vW7UhY9yQdKodSh-p8bnEkfprouh6gpMFoimc', '2026-09-06 13:21:48.024768'),
  ('ywu1xujy11a6d5sthinh4kddo7mr1xx6', '.eJxVjDsOwjAQBe_iGlnrJf5R0nMGa-21cQA5UpxUiLuTSCmgfTPz3iLQutSw9jyHkcVFKC1Ov2Ok9MxtJ_ygdp9kmtoyj1Huijxol7eJ8-t6uH8HlXrd6qS0teCyUgMaVyB67bA4SMn4mAfH2jIlOCNGVEgKikW7yZk0eMNFfL7kSzc6:1wyk3c:Kr_nUK6kmifLWvpS1CTYuAUUuLuSM7RQDCXfPcfAayQ', '2026-09-08 05:50:48.171395'),
  ('yyfqjmvxvw5d21iwvogwxrwmwcgjiwv2', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wylqT:VDseZVsPtkmzf7RQWpZRUWjApoD_KNd0vd19VwRAIYE', '2026-09-08 07:45:21.262874'),
  ('zdakb2gdrsu6p7dkxw5fruttn89ktdac', '.eJxVjEEOwiAQRe_C2hCYoUBduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWIE6_W6T04LaDfKd2m2Wa27pMUe6KPGiX1znz83K4fweVev3WGpVnwjwCMIEdmHTMgNkq58AAaj9qsqUk61EVNMoimsJu8FFZ74p4fwDFijbf:1wyThY:slZT6jqMBiiNg9Dd24QjCAQ3j-28IJ3RZcT2gFMb1ZA', '2026-09-07 12:22:56.759036'),
  ('zuswwb2rtclnopugyw1a8nvht2mgme0q', '.eJxVjMsOwiAQRf-FtSEwpeC4dN9vIAMzlaqBpI-V8d-1SRe6veec-1KRtrXEbZE5Tqwu6hzU6XdMlB9Sd8J3qremc6vrPCW9K_qgix4ay_N6uH8HhZbyrTMGlJCdYyQE7zE7A9aL63s2JFYsBdPDaAEIKCVmKwkwjZ2DgB2p9wcDKzgC:1wyqJc:vhu-wsy0Yk_rM51cXcmkncNPMp9D4BM_oK8mzyWP7c4', '2026-09-08 12:31:44.615717');

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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_complaint`
INSERT INTO `tbl_complaint` (`complaint_id`, `complaint_uuid`, `description`, `status`, `created_at`, `category`, `evidence_photo`, `admin_remarks`, `penalty_points_deducted`, `resolved_at`, `passenger_id`, `driver_id`, `trip_id`) VALUES
  (1, 'a29b3d4ce71640b084b05dc9eee77605', 'Driver demanded excess fare above meter rate during night commute and refused to use standard fare table.', 'Pending', '2026-08-23 04:09:30.663305', 'OVERCHARGING', '', NULL, 5, NULL, 3, 4, NULL),
  (5, '27540b2786a2488bb046fe596e3d050c', 'Driver demanded 50 rupees above the standard meter fare during late night commute from Pala bus stand.', 'Pending', '2026-08-25 06:25:53.078219', 'OVERCHARGING', '', NULL, 5, NULL, 20, 4, NULL),
  (6, 'aee3db04b08848cbb0055db3a5574ed7', 'Driver was talking loudly on phone while navigating intersection.', 'Resolved', '2026-08-22 09:25:53.078219', 'MISBEHAVIOR', '', 'Driver Rajesh was summoned, issued a formal safety caution, and 5 penalty points were deducted from reputation.', 5, '2026-08-23 09:25:53.078219', 2, 1, NULL);

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
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_driver`
INSERT INTO `tbl_driver` (`driver_id`, `name`, `phone_number`, `email`, `license_number`, `vehicle_number`, `vehicle_type`, `verification_status`, `qr_code`, `password`, `experience_years`, `verification_notes`, `verified_at`, `verification_token`, `reputation_score`, `total_trips`, `average_rating`, `driver_photo`, `license_doc`, `id_proof_doc`, `police_clearance_doc`, `qr_code_image`, `user_id`) VALUES
  (1, 'Rajesh Kumar', '+91 9447182930', 'driver_rajesh@saferide.org', 'KL-05-20180004521', 'KL-05-AT-4455', 'auto', 'Verified', '/media/driver_qrcodes/qr_KL-05-20180004521_1.png', 'pbkdf2_sha256$1500000$s5BmTCJ9FeyZ4JyEttwO4e$cEpT43Xask8eKJzZNV3EDYym2boP8nMx/oXqwPb3yVA=', 7, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:48.390508', '37644fd208ec44d2b0a7ff224b551ad2', 95.0, 664, 5.0, '', '', '', '', 'driver_qrcodes/qr_KL-05-20180004521_1.png', 4),
  (2, 'Anand Joseph', '+91 9847334455', 'driver_anand@saferide.org', 'KL-05-20150009812', 'KL-05-TX-1024', 'taxi', 'Verified', '/media/driver_qrcodes/qr_KL-05-20150009812_2.png', 'pbkdf2_sha256$1500000$dkJyokgiTgtFbgMGDbjEU0$C3eNLpcNqySs+AqI+dhM9VXq4uzqTnvDxv7w3PpESDY=', 9, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:50.023904', '25bab7460d5b4b9482b219dfc3d2f41d', 100.0, 418, 5.0, '', '', '', '', 'driver_qrcodes/qr_KL-05-20150009812_2.png', 5),
  (3, 'Suresh Babu', '+91 9745112233', 'driver_suresh@saferide.org', 'KL-05-20200003411', 'KL-05-CB-8890', 'cab', 'Verified', '/media/driver_qrcodes/qr_KL-05-20200003411_3.png', 'pbkdf2_sha256$1500000$brb2FYiWtSy8rvOH5f7Vf6$QdV6GdWFomxBJwXRzS7BRgklFl8GNcvaiVYGmjM22ek=', 4, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:51.542929', '58ce14e0766a4cf9b9c379f6bf63d7c3', 93.0, 215, 4.5, '', '', '', '', 'driver_qrcodes/qr_KL-05-20200003411_3.png', 6),
  (4, 'Vinod Mohan', '+91 9400223344', 'driver_vinod@saferide.org', 'KL-05-20240001290', 'KL-05-AT-9911', 'auto', 'Pending', NULL, 'pbkdf2_sha256$1500000$6PRFReWJH9t2mCrKibFcBs$Lq/+wjUfAI9MS316y/z0j+7/rr7EbcD9pWPCdaLXZV4=', 1, 'Awaiting physical RC verification', NULL, '0e0a406792c8431d8d60fca5a64937f6', 66.0, 12, 5.0, '', '', '', '', '', 7),
  (5, 'Pradeep Chandran', '+91 9447665544', 'driver_pradeep@saferide.org', 'KL-05-20170008821', 'KL-05-AT-7788', 'auto', 'Verified', '/media/driver_qrcodes/qr_KL-05-20170008821_5.png', 'pbkdf2_sha256$1500000$oFimqWMPwCCPV74BRTEpqY$8zZ0yR6pVxGISl5NdAoSHK7wYH6eol2RZonucWB66io=', 8, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:54.528353', '0e766821901b4928910dc447d77d3f1c', 93.0, 520, 4.5, '', '', '', '', 'driver_qrcodes/qr_KL-05-20170008821_5.png', 8),
  (6, 'Mathew Varghese', '+91 9847119988', 'driver_mathew@saferide.org', 'KL-35-20160007743', 'KL-35-TX-4521', 'taxi', 'Verified', '/media/driver_qrcodes/qr_KL-35-20160007743_6.png', 'pbkdf2_sha256$1500000$kJlNTxOE5ifRT86Q9Z7lZN$/S7btWVXsFbfnRDFO9OAaoEVZ6gdxGSaYz5APdMUvq4=', 10, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:56.223393', 'bbdfd1e9f4144ff9a01b84982d84d4d0', 93.0, 780, 4.5, '', '', '', '', 'driver_qrcodes/qr_KL-35-20160007743_6.png', 9),
  (7, 'Harikrishnan Nair', '+91 9745887766', 'driver_hari@saferide.org', 'KL-05-20190005512', 'KL-05-CB-3344', 'cab', 'Verified', '/media/driver_qrcodes/qr_KL-05-20190005512_7.png', 'pbkdf2_sha256$1500000$agqyrSDJwt9tnkWl7llvfv$1Jrc06hWqLQm3ve2smpWwXhUy2RwpvT0nwV6Vfty+Cc=', 5, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:57.933082', 'f0b8451da7bc4513bfc77f2d81048068', 93.0, 340, 4.5, '', '', '', '', 'driver_qrcodes/qr_KL-05-20190005512_7.png', 10),
  (8, 'Shaji Thomas', '+91 9495223311', 'driver_shaji@saferide.org', 'KL-05-20210006678', 'KL-05-EV-1205', 'cab', 'Verified', '/media/driver_qrcodes/qr_KL-05-20210006678_8.png', 'pbkdf2_sha256$1500000$GJA28sP6KSqf4PryyHEsqR$8GPdiyFDcwu4Iy9WRTRzmT9iNxBFqKDjAEcOV1gYz6c=', 3, 'Document verification completed and police clearance verified.', '2026-08-24 11:01:59.567807', '4a2c531981b34fdf9ff44a04200ac786', 100.0, 195, 5.0, '', '', '', '', 'driver_qrcodes/qr_KL-05-20210006678_8.png', 11),
  (9, 'Anoop Rajan', '+91 9605443322', 'driver_anoop@saferide.org', 'KL-35-20230009988', 'KL-35-AT-6622', 'auto', 'Pending', NULL, 'pbkdf2_sha256$1500000$ssD832GhfdKZEYtyOPnq0x$MIy76IXtI6bMTbkWBn7UsBqxqOh1HLmPK3Ni3hMbqRk=', 2, 'Awaiting physical RC verification', NULL, '3e5008d550e845d0b84f6a3f1ae08d4a', 85.0, 45, 5.0, '', '', '', '', '', 12),
  (10, 'Deepak K. S.', '+91 9946115500', 'driver_deepak@saferide.org', 'KL-07-20140003321', 'KL-07-CB-9080', 'cab', 'Verified', '/media/driver_qrcodes/qr_KL-07-20140003321_10.png', 'pbkdf2_sha256$1500000$5MIo90sfowgYLJRQeHQTJW$Ru4NttqmuqCxj2GAYiYETKBW3OCzKlT9zaExapZr0lQ=', 11, 'Document verification completed and police clearance verified.', '2026-08-24 11:02:02.951171', '61147761bd0740e49e8c25ab9ea48e66', 86.0, 910, 4.0, '', '', '', '', 'driver_qrcodes/qr_KL-07-20140003321_10.png', 13),
  (34, 'Manoj V. Nair', '+91 97467 28394', 'manoj.pala@gmail.com', 'KL-35-20220007733', 'KL-35-R-4512', 'auto', 'Pending', NULL, 'pbkdf2_sha256$1500000$WYJ5DwbZyVWo41MIeZTJJ1$+tBCo0DvUjuk5O77TIsKPgmPPYQKIHaV3EH9ITNtISA=', 4, 'Awaiting license inspection', NULL, '8d722e49d4c84843bac216d506350a0d', 63.0, 0, 4.5, '', '', '', '', '', 86);

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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_passenger`
INSERT INTO `tbl_passenger` (`passenger_id`, `name`, `email`, `phone_number`, `password`, `created_at`, `emergency_contact_1_name`, `emergency_contact_1_phone`, `emergency_contact_1_relation`, `emergency_contact_2_name`, `emergency_contact_2_phone`, `emergency_contact_2_relation`, `emergency_contact_3_name`, `emergency_contact_3_phone`, `emergency_contact_3_relation`, `address`, `profile_photo`, `user_id`) VALUES
  (1, 'Vyshnavi Venu', 'vyshnavi@sjcetpalai.ac.in', '+91 9847123456', 'pbkdf2_sha256$1500000$n0tjOBL02bEGRc0vFb7d2J$lc5mU91eR8yCW2vtc1iczntJtO2tlasbsqLGQR5YSeU=', '2026-08-23 04:09:12.705026', 'Venu Chandrasekharan Nair (Father)', '+91 9447012345', 'Parent', 'SJCET Security / Helpdesk', '+91 4822239700', 'Campus Security', NULL, NULL, 'Guardian', 'Palai, Kottayam, Kerala', '', 2),
  (2, 'Rahul Kurian', 'rahul.k@gmail.com', '+91 9895001122', 'pbkdf2_sha256$1500000$LqYbbCK759PfeVmuNI204T$PESJ7WpPXF74v1YAjBT3T7dzG25wVtFtt12NB79lmVE=', '2026-08-23 04:09:16.010659', 'Anita Kurian', '+91 9895009988', 'Sister', NULL, NULL, 'Friend', NULL, NULL, 'Guardian', 'Kottayam Road, Palai', '', 3),
  (6, 'Megha Nair', 'meghanair@gmail.com', '6789004321', 'pbkdf2_sha256$1500000$GhuD2Y0REsZbqqv6JOOpGn$PrtTxLwYlDFi8ParI33Qgjx9U+pXsy1APOk/tkE0lKU=', '2026-08-25 08:44:27.026672', 'ADHI', '7654321779', 'Family', NULL, NULL, 'Friend', NULL, NULL, 'Guardian', NULL, '', 20),
  (28, 'Rohit Menon', 'rohit.menon@gmail.com', '+91 97451 12389', 'pbkdf2_sha256$1500000$C3YhzK9IqhsPeMJtqgysjV$lS6DqcJ+LpV0Dn+1hgivoMb+WJpUEsK2qgS5luCk+9c=', '2026-08-25 09:24:20.992205', 'Deepa Menon (Mother)', '+91 97450 99887', 'Mother', 'Arun George (Roommate)', '+91 94951 44556', 'Friend', 'Emergency Police Helpline', '112', 'Emergency Service', NULL, '', 84),
  (29, 'Ananya Sharma', 'ananya.sharma@infopark.com', '+91 99462 87654', 'pbkdf2_sha256$1500000$SwsMF1HMxuLoqthrV9BGza$22sxjt8rK5tCmJ+Cu/o2OsOwtOSCUPA52LSyJD9g70o=', '2026-08-25 09:24:24.390066', 'Rajesh Sharma (Spouse)', '+91 99460 22110', 'Spouse', 'Kochi Police Control', '112', 'Police', 'Women Helpline Desk', '1091', 'Helpline', NULL, '', 85);

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
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_rating_review`
INSERT INTO `tbl_rating_review` (`rating_id`, `rating`, `review`, `created_at`, `driving_safety_rating`, `vehicle_cleanliness_rating`, `behavior_rating`, `fare_honesty_rating`, `driver_id`, `passenger_id`, `trip_id`) VALUES
  (9, 5, 'Very polite driver, smooth ride, and strict adherence to speed limits.', '2026-08-24 12:19:33.866805', 5, 5, 5, 5, 1, 2, 22),
  (10, 5, 'Comfortable taxi ride, clean vehicle, excellent safety protocol.', '2026-08-24 12:19:33.934012', 5, 5, 5, 5, 2, 2, 23),
  (25, 5, 'Exceptional service! Highly recommended.', '2026-08-25 09:13:01.416142', 5, 5, 5, 5, 1, 2, 44),
  (26, 5, 'Very polite driver! Drove at safe speed throughout the rain.', '2026-08-25 08:59:53.078219', 5, 5, 5, 5, 1, 2, 45),
  (27, 5, 'Extremely smooth and punctual commute. Clean auto-rickshaw.', '2026-08-24 08:47:53.078219', 5, 5, 5, 5, 4, 20, 46),
  (28, 5, 'Driver was courteous and charged strictly by the digital fare rate.', '2026-08-23 06:59:53.078219', 5, 5, 5, 5, 9, 84, 47),
  (29, 5, 'Helpful driver, verified QR badge matched the vehicle license plate perfectly.', '2026-08-21 23:49:53.078219', 5, 5, 5, 5, 8, 85, 48),
  (30, 4, 'Comfortable ride. Followed direct route without unnecessary deviation.', '2026-08-21 03:05:53.078219', 4, 5, 4, 4, 10, 2, 49),
  (31, 5, 'Prompt pickup near the college main gate. Recommended for night commuters.', '2026-08-20 04:44:53.078219', 5, 5, 5, 5, 1, 20, 50),
  (32, 5, 'Very polite driver! Drove at safe speed throughout the rain.', '2026-08-19 06:54:53.078219', 5, 5, 5, 5, 4, 84, 51),
  (33, 5, 'Extremely smooth and punctual commute. Clean auto-rickshaw.', '2026-08-18 00:54:53.078219', 5, 5, 5, 5, 9, 85, 52),
  (35, 5, 'Very polite driver! Drove at safe speed throughout the rain.', '2026-08-25 04:38:16.453764', 5, 5, 5, 5, 1, 2, 58),
  (36, 5, 'Extremely smooth and punctual commute. Clean auto-rickshaw.', '2026-08-24 07:30:16.453764', 5, 5, 5, 5, 4, 20, 59),
  (37, 5, 'Driver was courteous and charged strictly by the digital fare rate.', '2026-08-23 03:22:16.453764', 5, 5, 5, 5, 9, 84, 60),
  (38, 5, 'Helpful driver, verified QR badge matched the vehicle license plate perfectly.', '2026-08-22 01:28:16.453764', 5, 5, 5, 5, 8, 85, 61),
  (39, 4, 'Comfortable ride. Followed direct route without unnecessary deviation.', '2026-08-21 02:41:16.453764', 4, 5, 4, 4, 10, 2, 62),
  (40, 5, 'Prompt pickup near the college main gate. Recommended for night commuters.', '2026-08-20 00:28:16.453764', 5, 5, 5, 5, 1, 20, 63),
  (41, 5, 'Very polite driver! Drove at safe speed throughout the rain.', '2026-08-19 01:23:16.453764', 5, 5, 5, 5, 4, 84, 64),
  (42, 5, 'Extremely smooth and punctual commute. Clean auto-rickshaw.', '2026-08-18 09:26:16.453764', 5, 5, 5, 5, 9, 85, 65),
  (43, 5, 'Very polite driver! Drove at safe speed throughout the rain.', '2026-08-25 01:36:58.743836', 5, 5, 5, 5, 1, 2, 66),
  (44, 5, 'Extremely smooth and punctual commute. Clean auto-rickshaw.', '2026-08-24 04:39:58.743836', 5, 5, 5, 5, 4, 20, 67),
  (45, 5, 'Driver was courteous and charged strictly by the digital fare rate.', '2026-08-23 00:37:58.743836', 5, 5, 5, 5, 9, 84, 68),
  (46, 5, 'Helpful driver, verified QR badge matched the vehicle license plate perfectly.', '2026-08-22 06:37:58.743836', 5, 5, 5, 5, 8, 85, 69),
  (47, 4, 'Comfortable ride. Followed direct route without unnecessary deviation.', '2026-08-21 09:40:58.743836', 4, 5, 4, 4, 10, 2, 70),
  (48, 5, 'Prompt pickup near the college main gate. Recommended for night commuters.', '2026-08-20 09:34:58.743836', 5, 5, 5, 5, 1, 20, 71),
  (49, 5, 'Very polite driver! Drove at safe speed throughout the rain.', '2026-08-19 02:19:58.743836', 5, 5, 5, 5, 4, 84, 72),
  (50, 5, 'Extremely smooth and punctual commute. Clean auto-rickshaw.', '2026-08-18 01:24:58.743836', 5, 5, 5, 5, 9, 85, 73);

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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_sos_alert`
INSERT INTO `tbl_sos_alert` (`sos_id`, `alert_uuid`, `location`, `timestamp`, `status`, `latitude`, `longitude`, `location_name`, `admin_notes`, `dispatched_services`, `resolved_at`, `driver_id`, `passenger_id`, `trip_id`) VALUES
  (15, 'c512556363ec46109b37fbc852dc1664', 'Live GPS Distress Location', '2026-08-25 05:11:56.398674', 'Resolved', '9.684300', '76.685300', 'Test SafeRide Health Check Beacon', 'Passenger 1-Touch Emergency Distress Beacon triggered.', 'Local Police (112) & Emergency Contacts', NULL, NULL, 2, NULL),
  (18, '197ef3c4bab54d7886e4b856644e0106', 'Live GPS Emergency Distress Signal', '2026-08-25 08:53:45.141399', 'Resolved', '9.684300', '76.685300', 'Live GPS Emergency Distress Signal', 'Police Dispatch', 'Police (112), Campus Control, Admin Console', '2026-08-25 09:21:56.196622', NULL, 2, NULL),
  (19, '8435a72f68504ae2aa7ab9b81f0d2093', 'Live GPS Emergency Distress Signal', '2026-08-25 08:53:49.574072', 'Resolved', '9.684300', '76.685300', 'Live GPS Emergency Distress Signal', 'Dispatched emergency unit. Passenger safe.', 'Police (112), Campus Control, Admin Console', '2026-08-25 09:21:26.624867', NULL, 20, NULL),
  (23, '37afbc78e923444db4c194f3de171f5f', 'Live GPS Distress Location', '2026-08-25 09:21:53.078219', 'Active', '9.684300', '76.685300', 'Near SJCET Main Campus Gate, Palai', NULL, 'Palai Police Station (112), Women Helpline (1091)', NULL, 4, 20, NULL),
  (24, '7358e4847d954455aa54b93f312dc63f', 'Live GPS Distress Location', '2026-08-24 09:25:53.078219', 'Resolved', '9.712500', '76.683000', 'Pala Private Bus Stand Terminal', '1-Touch test alert triggered by commuter. Passenger confirmed safe.', 'Local Police (112) & Emergency Contacts', '2026-08-24 09:35:53.078219', 1, 2, NULL),
  (30, 'e0792d6242e046e5ad49943a5f728ac5', 'Test SafeRide Health Check Beacon', '2026-08-29 07:56:37.485905', 'Active', '9.684300', '76.685300', 'Test SafeRide Health Check Beacon', NULL, 'Police (112), Campus Control, Admin Console', NULL, NULL, 2, NULL);

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
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_trip`
INSERT INTO `tbl_trip` (`trip_id`, `trip_uuid`, `start_location`, `end_location`, `start_time`, `end_time`, `status`, `pickup_location_name`, `pickup_latitude`, `pickup_longitude`, `drop_location_name`, `drop_latitude`, `drop_longitude`, `live_latitude`, `live_longitude`, `live_updated_at`, `share_token`, `driver_id`, `passenger_id`, `boarding_address`, `boarding_latitude`, `boarding_longitude`, `current_latitude`, `current_longitude`, `destination_address`, `destination_latitude`, `destination_longitude`) VALUES
  (22, '82b8af9eff0f4f07b8345d7cc4dc2ea0', 'Current Boarding Point', 'Pala KSRTC Bus Stand', '2026-08-24 10:19:33.847860', '2026-08-24 10:34:33.847860', 'SOS_Triggered', 'Current Location', '9.684300', '76.685300', NULL, '9.691200', '76.690400', '9.685000', '76.686000', '2026-08-27 15:35:02.489505', '5c198be2a7964278b668b3efcba8ef6a', 1, 2, 'St. Thomas College Gate, Palai', '9.684300', '76.685300', '9.685000', '76.686000', 'Pala KSRTC Bus Stand', '9.691200', '76.690400'),
  (23, 'f9e305bd9ec6484e881041b9270b67be', 'Current Boarding Point', 'Mar Sleeva Medicity, Palai', '2026-08-23 09:19:33.847860', '2026-08-23 09:49:33.847860', 'Completed', 'Current Location', '9.688000', '76.687000', NULL, '9.712600', '76.685400', '9.684300', '76.685300', '2026-08-24 12:19:33.911657', '4f4d73940a12456cb0ad6ab630ad7a3e', 2, 2, 'Palai Private Bus Stand', '9.688000', '76.687000', '9.684300', '76.685300', 'Mar Sleeva Medicity, Palai', '9.712600', '76.685400'),
  (24, '0cb7ca9da2e84bf3b5b65a4093309187', 'Current Boarding Point', 'St. Joseph\'s College of Engineering, Choondacherry', '2026-08-24 11:39:33.847860', '2026-08-24 12:04:33.847860', 'Completed', 'Current Location', '9.687500', '76.684800', NULL, '9.664000', '76.698000', '9.684300', '76.685300', '2026-08-24 12:19:33.967773', '47c52b98f0194c11826ccb46dddf9630', 1, 2, 'Pala Municipal Town Hall', '9.687500', '76.684800', '9.684300', '76.685300', 'St. Joseph\'s College of Engineering, Choondacherry', '9.664000', '76.698000'),
  (44, '7412a82c160444678a55272080fa7ba0', 'Current Boarding Point', NULL, '2026-08-25 09:13:00.498567', NULL, 'Active', 'Current Location', '9.684300', '76.685300', NULL, NULL, NULL, '9.684300', '76.685300', '2026-08-25 09:13:00.498567', 'dfcaaa850c604c9ea6482a21ca186aad', 1, 2, 'Current Boarding Point', '9.684300', '76.685300', '9.684300', '76.685300', NULL, NULL, NULL),
  (45, '0426a715475e425eb7a88f76dc6e064e', 'Current Boarding Point', 'Palai KSRTC Bus Terminal', '2026-08-25 08:25:53.078219', '2026-08-25 08:59:53.078219', 'Completed', 'Current Location', '9.684300', '76.685300', NULL, '9.711800', '76.684400', '9.711800', '76.684400', '2026-08-25 09:25:53.113893', 'b10c42717db44d3aa51ca98a549d8f24', 1, 2, 'St. Joseph\'s College of Engineering & Technology, Palai', '9.684300', '76.685300', '9.711800', '76.684400', 'Palai KSRTC Bus Terminal', '9.711800', '76.684400'),
  (46, '621d955c005b4499bdbb7302a4856032', 'Current Boarding Point', 'Alphonsa College, Palai', '2026-08-24 08:25:53.078219', '2026-08-24 08:47:53.078219', 'Completed', 'Current Location', '9.712500', '76.683000', NULL, '9.702000', '76.689000', '9.702000', '76.689000', '2026-08-25 09:25:53.317674', 'e6ba9390adc7478fadafd8811dc83eb2', 4, 20, 'Pala Private Bus Stand', '9.712500', '76.683000', '9.702000', '76.689000', 'Alphonsa College, Palai', '9.702000', '76.689000'),
  (47, '68dbfa9b425949dd8c31b3d764fb832a', 'Current Boarding Point', 'Mar Sleeva Medicity, Cherpunkal', '2026-08-23 06:25:53.078219', '2026-08-23 06:59:53.078219', 'Completed', 'Current Location', '9.713000', '76.685000', NULL, '9.664000', '76.612000', '9.664000', '76.612000', '2026-08-25 09:25:53.385468', 'a50bf8e2fb7b4903900140bc6a9c271b', 9, 84, 'Pala Town Centre', '9.713000', '76.685000', '9.664000', '76.612000', 'Mar Sleeva Medicity, Cherpunkal', '9.664000', '76.612000'),
  (48, '61726a481f8f4757ab6a4477a4a70e1b', 'Current Boarding Point', 'Kottayam Railway Station', '2026-08-21 23:25:53.078219', '2026-08-21 23:49:53.078219', 'Completed', 'Current Location', '9.715000', '76.681000', NULL, '9.589000', '76.522000', '9.589000', '76.522000', '2026-08-25 09:25:53.433392', '594d9d871a6048c3a6cdf3c259363138', 8, 85, 'St. Thomas College, Palai', '9.715000', '76.681000', '9.589000', '76.522000', 'Kottayam Railway Station', '9.589000', '76.522000'),
  (49, '5bad4d794ab2425f9bdc9c748d3d4568', 'Current Boarding Point', 'Kottayam KSRTC Stand', '2026-08-21 02:25:53.078219', '2026-08-21 03:05:53.078219', 'Completed', 'Current Location', '9.624000', '76.538000', NULL, '9.591000', '76.524000', '9.591000', '76.524000', '2026-08-25 09:25:53.499246', 'e44fcf20ca2b47d78647f8af74952094', 10, 2, 'Kottayam Medical College', '9.624000', '76.538000', '9.591000', '76.524000', 'Kottayam KSRTC Stand', '9.591000', '76.524000'),
  (50, '2cc6c1058ba445968c3d2d3e14e76b04', 'Current Boarding Point', 'Palai KSRTC Bus Terminal', '2026-08-20 04:25:53.078219', '2026-08-20 04:44:53.078219', 'Completed', 'Current Location', '9.684300', '76.685300', NULL, '9.711800', '76.684400', '9.711800', '76.684400', '2026-08-25 09:25:53.556094', '99d8213597c64b18a819f4c1a0c7ccdb', 1, 20, 'St. Joseph\'s College of Engineering & Technology, Palai', '9.684300', '76.685300', '9.711800', '76.684400', 'Palai KSRTC Bus Terminal', '9.711800', '76.684400'),
  (51, '92ef7b394e0149e382609659a33630ec', 'Current Boarding Point', 'Alphonsa College, Palai', '2026-08-19 06:25:53.078219', '2026-08-19 06:54:53.078219', 'Completed', 'Current Location', '9.712500', '76.683000', NULL, '9.702000', '76.689000', '9.702000', '76.689000', '2026-08-25 09:25:53.612456', '14c0800d461946258a9287cf4249b8a4', 4, 84, 'Pala Private Bus Stand', '9.712500', '76.683000', '9.702000', '76.689000', 'Alphonsa College, Palai', '9.702000', '76.689000'),
  (52, '5363f67535b54481a766a674cf846553', 'Current Boarding Point', 'Mar Sleeva Medicity, Cherpunkal', '2026-08-18 00:25:53.078219', '2026-08-18 00:54:53.078219', 'Completed', 'Current Location', '9.713000', '76.685000', NULL, '9.664000', '76.612000', '9.664000', '76.612000', '2026-08-25 09:25:53.666310', '58abc82444c74062952f1c39bebc210d', 9, 85, 'Pala Town Centre', '9.713000', '76.685000', '9.664000', '76.612000', 'Mar Sleeva Medicity, Cherpunkal', '9.664000', '76.612000'),
  (54, 'c4fe3af4f3a24df0b9c429d244441d5c', 'Current Boarding Point', 'Pala KSRTC Bus Stand', '2026-08-25 10:00:04.364413', NULL, 'Active', 'Current Location', '9.684300', '76.685300', NULL, '9.691200', '76.690400', '9.684300', '76.685300', '2026-08-25 10:00:04.364413', '46794e7fcc074638b643bbc7cf503562', 1, 2, 'St. Thomas College Gate, Palai', '9.684300', '76.685300', '9.684300', '76.685300', 'Pala KSRTC Bus Stand', '9.691200', '76.690400'),
  (58, '835c4d487d964c1ca8f0cb0588e7632f', 'Current Boarding Point', 'Palai KSRTC Bus Terminal', '2026-08-25 04:03:16.453764', '2026-08-25 04:38:16.453764', 'Completed', 'Current Location', '9.684300', '76.685300', NULL, '9.711800', '76.684400', '9.711800', '76.684400', '2026-08-25 10:03:16.453764', '8232e0b50ddf4aed8a31f6f6796ee52e', 1, 2, 'St. Joseph\'s College of Engineering & Technology, Palai', '9.684300', '76.685300', '9.711800', '76.684400', 'Palai KSRTC Bus Terminal', '9.711800', '76.684400'),
  (59, 'cecb3b6d3d4d4736a627e5b6ee57d790', 'Current Boarding Point', 'Alphonsa College, Palai', '2026-08-24 07:03:16.453764', '2026-08-24 07:30:16.453764', 'Completed', 'Current Location', '9.712500', '76.683000', NULL, '9.702000', '76.689000', '9.702000', '76.689000', '2026-08-25 10:03:16.520768', '64bd734bf4ad49ff945324ee8c720ace', 4, 20, 'Pala Private Bus Stand', '9.712500', '76.683000', '9.702000', '76.689000', 'Alphonsa College, Palai', '9.702000', '76.689000'),
  (60, 'a2e7bc1f82a543c4aae4d2c275e6139d', 'Current Boarding Point', 'Mar Sleeva Medicity, Cherpunkal', '2026-08-23 03:03:16.453764', '2026-08-23 03:22:16.453764', 'Completed', 'Current Location', '9.713000', '76.685000', NULL, '9.664000', '76.612000', '9.664000', '76.612000', '2026-08-25 10:03:16.705103', 'c6f0b8d23f054541a605e3442cd28f8f', 9, 84, 'Pala Town Centre', '9.713000', '76.685000', '9.664000', '76.612000', 'Mar Sleeva Medicity, Cherpunkal', '9.664000', '76.612000'),
  (61, 'cc5eebf279084764834e4e5d14bc07c1', 'Current Boarding Point', 'Kottayam Railway Station', '2026-08-22 01:03:16.453764', '2026-08-22 01:28:16.453764', 'Completed', 'Current Location', '9.715000', '76.681000', NULL, '9.589000', '76.522000', '9.589000', '76.522000', '2026-08-25 10:03:16.817758', '42af19f5fb0b43d4bc600a4f7cd9446c', 8, 85, 'St. Thomas College, Palai', '9.715000', '76.681000', '9.589000', '76.522000', 'Kottayam Railway Station', '9.589000', '76.522000'),
  (62, '454bc782b53f46559a5f0812fb94cb83', 'Current Boarding Point', 'Kottayam KSRTC Stand', '2026-08-21 02:03:16.453764', '2026-08-21 02:41:16.453764', 'Completed', 'Current Location', '9.624000', '76.538000', NULL, '9.591000', '76.524000', '9.591000', '76.524000', '2026-08-25 10:03:16.854066', 'f0eec393f3164a3abd7f6cf8e489c6dd', 10, 2, 'Kottayam Medical College', '9.624000', '76.538000', '9.591000', '76.524000', 'Kottayam KSRTC Stand', '9.591000', '76.524000'),
  (63, '0ee2ccc80a8f4ecc85044d341f7b5707', 'Current Boarding Point', 'Palai KSRTC Bus Terminal', '2026-08-20 00:03:16.453764', '2026-08-20 00:28:16.453764', 'Completed', 'Current Location', '9.684300', '76.685300', NULL, '9.711800', '76.684400', '9.711800', '76.684400', '2026-08-25 10:03:16.903809', '872c519877b5482aa37389daf71b9b44', 1, 20, 'St. Joseph\'s College of Engineering & Technology, Palai', '9.684300', '76.685300', '9.711800', '76.684400', 'Palai KSRTC Bus Terminal', '9.711800', '76.684400'),
  (64, '278928cc5586409bbb109447a4d47c5a', 'Current Boarding Point', 'Alphonsa College, Palai', '2026-08-19 01:03:16.453764', '2026-08-19 01:23:16.453764', 'Completed', 'Current Location', '9.712500', '76.683000', NULL, '9.702000', '76.689000', '9.702000', '76.689000', '2026-08-25 10:03:16.952092', '07706cb3bef747c084e88f7793fa44ad', 4, 84, 'Pala Private Bus Stand', '9.712500', '76.683000', '9.702000', '76.689000', 'Alphonsa College, Palai', '9.702000', '76.689000'),
  (65, '9c17dd57ba0747c787c64d20b21a4f72', 'Current Boarding Point', 'Mar Sleeva Medicity, Cherpunkal', '2026-08-18 09:03:16.453764', '2026-08-18 09:26:16.453764', 'Completed', 'Current Location', '9.713000', '76.685000', NULL, '9.664000', '76.612000', '9.664000', '76.612000', '2026-08-25 10:03:17.004332', 'df1379d5f924403d90cbb0de3bcc1cb1', 9, 85, 'Pala Town Centre', '9.713000', '76.685000', '9.664000', '76.612000', 'Mar Sleeva Medicity, Cherpunkal', '9.664000', '76.612000'),
  (66, '6b514a6ff69d455b8375c827c1645fbb', 'Current Boarding Point', 'Palai KSRTC Bus Terminal', '2026-08-25 01:04:58.743836', '2026-08-25 01:36:58.743836', 'Completed', 'Current Location', '9.684300', '76.685300', NULL, '9.711800', '76.684400', '9.711800', '76.684400', '2026-08-25 10:04:58.759932', '16eb550e67ef4adbac301fa51579a011', 1, 2, 'St. Joseph\'s College of Engineering & Technology, Palai', '9.684300', '76.685300', '9.711800', '76.684400', 'Palai KSRTC Bus Terminal', '9.711800', '76.684400'),
  (67, '66806eb8ced045f8bbf8e1761d987625', 'Current Boarding Point', 'Alphonsa College, Palai', '2026-08-24 04:04:58.743836', '2026-08-24 04:39:58.743836', 'Completed', 'Current Location', '9.712500', '76.683000', NULL, '9.702000', '76.689000', '9.702000', '76.689000', '2026-08-25 10:04:58.900528', 'a59b4747d50c4422a131cfe569a69e2e', 4, 20, 'Pala Private Bus Stand', '9.712500', '76.683000', '9.702000', '76.689000', 'Alphonsa College, Palai', '9.702000', '76.689000'),
  (68, '219adf31263945338b8f6ea9a8b80003', 'Current Boarding Point', 'Mar Sleeva Medicity, Cherpunkal', '2026-08-23 00:04:58.743836', '2026-08-23 00:37:58.743836', 'Completed', 'Current Location', '9.713000', '76.685000', NULL, '9.664000', '76.612000', '9.664000', '76.612000', '2026-08-25 10:04:58.931904', '1e629cb147c14df69bba90391378edf9', 9, 84, 'Pala Town Centre', '9.713000', '76.685000', '9.664000', '76.612000', 'Mar Sleeva Medicity, Cherpunkal', '9.664000', '76.612000'),
  (69, '43aa2573d4954985b9024d11d77cf926', 'Current Boarding Point', 'Kottayam Railway Station', '2026-08-22 06:04:58.743836', '2026-08-22 06:37:58.743836', 'Completed', 'Current Location', '9.715000', '76.681000', NULL, '9.589000', '76.522000', '9.589000', '76.522000', '2026-08-25 10:04:58.995078', '071855dc1bc6433eb4da98b39020e0bc', 8, 85, 'St. Thomas College, Palai', '9.715000', '76.681000', '9.589000', '76.522000', 'Kottayam Railway Station', '9.589000', '76.522000'),
  (70, 'c56729e982b944b98a68fe0bb36ecfc9', 'Current Boarding Point', 'Kottayam KSRTC Stand', '2026-08-21 09:04:58.743836', '2026-08-21 09:40:58.743836', 'Completed', 'Current Location', '9.624000', '76.538000', NULL, '9.591000', '76.524000', '9.591000', '76.524000', '2026-08-25 10:04:59.143784', '79de5df660a1415fa619b1c29357be49', 10, 2, 'Kottayam Medical College', '9.624000', '76.538000', '9.591000', '76.524000', 'Kottayam KSRTC Stand', '9.591000', '76.524000'),
  (71, '85153f1ca69947f197f9fb3ffa7b8da1', 'Current Boarding Point', 'Palai KSRTC Bus Terminal', '2026-08-20 09:04:58.743836', '2026-08-20 09:34:58.743836', 'Completed', 'Current Location', '9.684300', '76.685300', NULL, '9.711800', '76.684400', '9.711800', '76.684400', '2026-08-25 10:04:59.190497', 'ef27aff1eb3d487db277ea4e92e8ae45', 1, 20, 'St. Joseph\'s College of Engineering & Technology, Palai', '9.684300', '76.685300', '9.711800', '76.684400', 'Palai KSRTC Bus Terminal', '9.711800', '76.684400'),
  (72, 'a9758fece1d947138b07fd6699c652ac', 'Current Boarding Point', 'Alphonsa College, Palai', '2026-08-19 02:04:58.743836', '2026-08-19 02:19:58.743836', 'Completed', 'Current Location', '9.712500', '76.683000', NULL, '9.702000', '76.689000', '9.702000', '76.689000', '2026-08-25 10:04:59.235471', '6ace3156da944f85a82a14821336e6f6', 4, 84, 'Pala Private Bus Stand', '9.712500', '76.683000', '9.702000', '76.689000', 'Alphonsa College, Palai', '9.702000', '76.689000'),
  (73, 'e0568677caff44848af52a5ceb16b65b', 'Current Boarding Point', 'Mar Sleeva Medicity, Cherpunkal', '2026-08-18 01:04:58.743836', '2026-08-18 01:24:58.743836', 'Completed', 'Current Location', '9.713000', '76.685000', NULL, '9.664000', '76.612000', '9.664000', '76.612000', '2026-08-25 10:04:59.298115', '0231026f1eeb479fb401f23cfe8eef43', 9, 85, 'Pala Town Centre', '9.713000', '76.685000', '9.664000', '76.612000', 'Mar Sleeva Medicity, Cherpunkal', '9.664000', '76.612000');

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
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table `tbl_user`
INSERT INTO `tbl_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `phone`, `avatar`, `created_at`, `updated_at`) VALUES
  (1, 'pbkdf2_sha256$1500000$oKOszMvDDe2zpray0vv3qp$FjMvju42VRMVcOixjswGPsv2KoMxrEd9uetuSHxCzr0=', '2026-08-29 07:56:35.776099', 1, 'admin', 'SafeRide', 'Administrator', 'admin@saferide.org', 1, 1, '2026-08-23 04:09:05.639717', 'ADMIN', NULL, '', '2026-08-23 04:09:05.640715', '2026-08-25 10:04:42.441027'),
  (2, 'pbkdf2_sha256$1500000$BQvccKXtWMZAfOatC54ChV$EjsMflevUs4Ui2AGecX2FCVerHT6si1itoPnBbSVzxs=', '2026-08-29 07:56:37.423432', 0, 'vyshnavi', 'Vyshnavi', 'Venu', 'vyshnavi@sjcetpalai.ac.in', 0, 1, '2026-08-23 04:09:09.087679', 'PASSENGER', '+91 9847123456', '', '2026-08-23 04:09:09.088722', '2026-08-25 10:04:44.240312'),
  (3, 'pbkdf2_sha256$1500000$LqYbbCK759PfeVmuNI204T$PESJ7WpPXF74v1YAjBT3T7dzG25wVtFtt12NB79lmVE=', NULL, 0, 'rahul', 'Rahul', 'Kurian', 'rahul.k@gmail.com', 0, 1, '2026-08-23 04:09:12.728602', 'PASSENGER', '+91 9895001122', '', '2026-08-23 04:09:12.729601', '2026-08-24 11:01:46.988777'),
  (4, 'pbkdf2_sha256$1500000$TFs4QlrZE68ZY7X0Po2bCc$Nbf/yu0yKn2S4gut83pyqegKmW89tSZXFVLYh3w7GT4=', '2026-08-29 07:56:34.177100', 0, 'driver_rajesh', 'Rajesh', 'Kumar', 'driver_rajesh@saferide.org', 0, 1, '2026-08-23 04:09:16.087407', 'DRIVER', '+91 9447182930', '', '2026-08-23 04:09:16.088456', '2026-08-25 10:04:49.955571'),
  (5, 'pbkdf2_sha256$1500000$Y7wkVy4L2GLxoKDuES64a1$jnFG6mZAcW6AuJhMaV2iom4VWjO4uoCAcb1HU5IxdX4=', '2026-08-29 07:56:17.544556', 0, 'driver_anand', 'Anand', 'Joseph', 'driver_anand@saferide.org', 0, 1, '2026-08-23 04:09:19.911832', 'DRIVER', '+91 9847334455', '', '2026-08-23 04:09:19.913869', '2026-08-24 12:19:33.752828'),
  (6, 'pbkdf2_sha256$1500000$n1CXMx0U0W5aYZPQpboK5K$y5v2lQFpKMgPU7/cTr/jArE8ExZlfgzSNlGQqaKVTgg=', '2026-08-29 07:56:19.050481', 0, 'driver_suresh', 'Suresh', 'Babu', 'driver_suresh@saferide.org', 0, 1, '2026-08-23 04:09:23.474448', 'DRIVER', '+91 9745112233', '', '2026-08-23 04:09:23.474448', '2026-08-25 10:04:57.280515'),
  (7, 'pbkdf2_sha256$1500000$tZbLdv1YO2MKqsZZTQ0Aj7$s7XAAjASXbxV85v1ySjjkADZAmxA0ZGsnZmm8iJ7AIU=', '2026-08-29 07:56:20.502559', 0, 'driver_vinod', 'Vinod', 'Mohan', 'driver_vinod@saferide.org', 0, 1, '2026-08-23 04:09:26.866820', 'DRIVER', '+91 9400223344', '', '2026-08-23 04:09:26.867816', '2026-08-25 10:04:51.474809'),
  (8, 'pbkdf2_sha256$1500000$oFimqWMPwCCPV74BRTEpqY$8zZ0yR6pVxGISl5NdAoSHK7wYH6eol2RZonucWB66io=', '2026-08-29 07:56:22.077678', 0, 'driver_pradeep', 'Pradeep', 'Chandran', 'driver_pradeep@saferide.org', 0, 1, '2026-08-24 05:17:32.674813', 'DRIVER', '+91 9447665544', '', '2026-08-24 05:17:32.675808', '2026-08-24 11:01:54.479704'),
  (9, 'pbkdf2_sha256$1500000$kJlNTxOE5ifRT86Q9Z7lZN$/S7btWVXsFbfnRDFO9OAaoEVZ6gdxGSaYz5APdMUvq4=', '2026-08-29 07:56:23.549484', 0, 'driver_mathew', 'Mathew', 'Varghese', 'driver_mathew@saferide.org', 0, 1, '2026-08-24 05:17:37.166413', 'DRIVER', '+91 9847119988', '', '2026-08-24 05:17:37.166413', '2026-08-24 11:01:56.171868'),
  (10, 'pbkdf2_sha256$1500000$agqyrSDJwt9tnkWl7llvfv$1Jrc06hWqLQm3ve2smpWwXhUy2RwpvT0nwV6Vfty+Cc=', '2026-08-29 07:56:24.984657', 0, 'driver_hari', 'Harikrishnan', 'Nair', 'driver_hari@saferide.org', 0, 1, '2026-08-24 05:17:41.066888', 'DRIVER', '+91 9745887766', '', '2026-08-24 05:17:41.067916', '2026-08-24 11:01:57.899575'),
  (11, 'pbkdf2_sha256$1500000$ln4KNxwfdTLN68jti0Ajfo$85ZSzFlf2oP/20AjsSXkAJurMYzP45JRMSbjtrBdVP0=', '2026-08-29 07:56:26.411299', 0, 'driver_shaji', 'Shaji', 'Thomas', 'driver_shaji@saferide.org', 0, 1, '2026-08-24 05:17:45.089489', 'DRIVER', '+91 9495223311', '', '2026-08-24 05:17:45.090522', '2026-08-25 10:04:54.377660'),
  (12, 'pbkdf2_sha256$1500000$stv2g8QIiQPznmFZHrsTsm$I0odATaQzyf7p7sRA72y8u/7OQfhkmzHCMZsqavdV1M=', '2026-08-29 07:56:27.909799', 0, 'driver_anoop', 'Anoop', 'Rajan', 'driver_anoop@saferide.org', 0, 1, '2026-08-24 05:17:48.572394', 'DRIVER', '+91 9605443322', '', '2026-08-24 05:17:48.573391', '2026-08-25 10:04:52.891919'),
  (13, 'pbkdf2_sha256$1500000$eWpvTdYF530vL5zdbUqNaX$OQEo/+YtMUAj+Ig+PysnijvkIJCvnLOhqdPSRtyUKlw=', '2026-08-29 07:56:29.392889', 0, 'driver_deepak', 'Deepak', 'K. S.', 'driver_deepak@saferide.org', 0, 1, '2026-08-24 05:17:51.026068', 'DRIVER', '+91 9946115500', '', '2026-08-24 05:17:51.026068', '2026-08-25 10:04:55.812404'),
  (20, 'pbkdf2_sha256$1500000$DqmbwytCJZvbi5h9Ob3J5I$xDCRU2y7MEycWgRLFnmmTlHON678nOQ/1EVBZyHJjzM=', '2026-08-25 09:31:41.979555', 0, 'meghanair', 'Megha', 'Nair', 'meghanair@gmail.com', 0, 1, '2026-08-25 08:44:22.058426', 'PASSENGER', '6789004321', '', '2026-08-25 08:44:26.854258', '2026-08-25 10:04:45.740215'),
  (84, 'pbkdf2_sha256$1500000$QYnvMBIlNzTwB433xVi7YM$Pgv9do6NFbZm8gF3JmS0gpfWIGkDPRhT9kRspNqU4Os=', NULL, 0, 'rohit_menon', 'Rohit', 'Menon', 'rohit.menon@gmail.com', 0, 1, '2026-08-25 09:24:17.914093', 'PASSENGER', '+91 97451 12389', '', '2026-08-25 09:24:17.915079', '2026-08-25 10:04:47.149238'),
  (85, 'pbkdf2_sha256$1500000$LSUcKSVJByW7EAPJfiB7Ll$baIIdr+WgvfgFqCaMgm93ekD9+qZA+qtKItDRYZnFkc=', NULL, 0, 'ananya_s', 'Ananya', 'Sharma', 'ananya.sharma@infopark.com', 0, 1, '2026-08-25 09:24:21.058154', 'PASSENGER', '+91 99462 87654', '', '2026-08-25 09:24:21.058154', '2026-08-25 10:04:48.563904'),
  (86, 'pbkdf2_sha256$1500000$SB9aTBNcIB5E7dfg4qH0aB$EibX95BixApjJilhditubX+KsgSM53tEPxv+GaV4gRI=', '2026-08-29 07:56:30.904752', 0, 'driver_manoj', 'Manoj', 'V. Nair', 'manoj.pala@gmail.com', 0, 1, '2026-08-25 09:24:43.416568', 'DRIVER', '+91 97467 28394', '', '2026-08-25 09:24:43.416568', '2026-08-25 10:04:58.683317');

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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
  (10, '/media/driver_docs/license/lic_KL-07-20140003321.pdf', '/media/vehicle_docs/rc/rc_KL-07-CB-9080.pdf', '2026-08-24 05:17:54.842550', '', '', 10),
  (11, 'KL-35-20220007733_verified.pdf', 'KL-35-R-4512_rc.pdf', '2026-08-25 09:25:53.071237', '', '', 34);

SET FOREIGN_KEY_CHECKS=1;
