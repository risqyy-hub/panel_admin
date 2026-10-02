-- =====================================================================
-- ADMIN DOKTER - Database Schema
-- Database : admin_dokter
-- Engine   : MariaDB / MySQL (InnoDB)
-- Cara pakai: mysql -u root < database/schema.sql
-- =====================================================================

CREATE DATABASE IF NOT EXISTS `admin_dokter`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `admin_dokter`;

-- =====================================================================
-- TABEL: users
-- Menyimpan semua akun: admin, dokter, dan user biasa.
-- Password WAJIB disimpan dalam bentuk hash (bcrypt), bukan plaintext.
-- =====================================================================
DROP TABLE IF EXISTS `reports`;
DROP TABLE IF EXISTS `report_categories`;
DROP TABLE IF EXISTS `doctor_documents`;
DROP TABLE IF EXISTS `doctors`;
DROP TABLE IF EXISTS `sliders`;
DROP TABLE IF EXISTS `admin_activity_logs`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id`          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `name`        VARCHAR(120)    NOT NULL,
  `email`       VARCHAR(160)    NOT NULL,
  `password`    VARCHAR(255)    NOT NULL,
  `phone`       VARCHAR(30)     DEFAULT NULL,
  `role`        VARCHAR(20)     NOT NULL DEFAULT 'user',   -- admin | doctor | user
  `status`      VARCHAR(20)     NOT NULL DEFAULT 'active', -- active | inactive | suspended
  `avatar`      VARCHAR(255)    DEFAULT NULL,
  `created_at`  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_email` (`email`),
  KEY `idx_users_role` (`role`),
  KEY `idx_users_status` (`status`),
  KEY `idx_users_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- TABEL: doctors
-- Relasi 1 : 1 dengan users (user_id UNIQUE).
-- =====================================================================
CREATE TABLE `doctors` (
  `id`                  INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `user_id`             INT UNSIGNED    NOT NULL,
  `specialization`      VARCHAR(120)    DEFAULT NULL,
  `license_number`      VARCHAR(80)     DEFAULT NULL,   -- Nomor STR/SIP
  `education`           VARCHAR(255)    DEFAULT NULL,
  `experience`          VARCHAR(255)    DEFAULT NULL,
  `bio`                 TEXT            DEFAULT NULL,
  `verification_status` VARCHAR(20)     NOT NULL DEFAULT 'pending', -- pending | approved | rejected
  `rejection_reason`    TEXT            DEFAULT NULL,
  `verified_at`         TIMESTAMP       NULL DEFAULT NULL,
  `is_active`           TINYINT(1)      NOT NULL DEFAULT 1,
  `created_at`          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_doctors_user_id` (`user_id`),
  KEY `idx_doctors_verification` (`verification_status`),
  KEY `idx_doctors_specialization` (`specialization`),
  CONSTRAINT `fk_doctors_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- TABEL: doctor_documents
-- Dokumen pendukung: STR, SIP, ijazah, sertifikat, lainnya.
-- =====================================================================
CREATE TABLE `doctor_documents` (
  `id`                  INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `doctor_id`           INT UNSIGNED NOT NULL,
  `document_type`       VARCHAR(30)  NOT NULL DEFAULT 'lainnya', -- str | sip | ijazah | sertifikat | lainnya
  `document_path`       VARCHAR(255) NOT NULL,
  `verification_status` VARCHAR(20)  NOT NULL DEFAULT 'pending',  -- pending | approved | rejected
  `created_at`          TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`          TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_docs_doctor` (`doctor_id`),
  KEY `idx_docs_type` (`document_type`),
  CONSTRAINT `fk_docs_doctor`
    FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- TABEL: sliders
-- Banner yang tampil di halaman user.
-- =====================================================================
CREATE TABLE `sliders` (
  `id`          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title`       VARCHAR(150) NOT NULL,
  `description` VARCHAR(500) DEFAULT NULL,
  `image`       VARCHAR(255) NOT NULL,
  `link`        VARCHAR(255) DEFAULT NULL,
  `sort_order`  INT          NOT NULL DEFAULT 0,
  `status`      VARCHAR(20)  NOT NULL DEFAULT 'active', -- active | inactive
  `created_at`  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_sliders_status` (`status`),
  KEY `idx_sliders_sort` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- TABEL: report_categories
-- Kategori laporan user terhadap dokter.
-- =====================================================================
CREATE TABLE `report_categories` (
  `id`          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name`        VARCHAR(100) NOT NULL,
  `description` VARCHAR(255) DEFAULT NULL,
  `created_at`  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_report_categories_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- TABEL: reports
-- Laporan user terhadap dokter.
-- CATATAN: dokter TIDAK otomatis dihukum - admin review dulu.
-- =====================================================================
CREATE TABLE `reports` (
  `id`          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id`     INT UNSIGNED NOT NULL,
  `doctor_id`   INT UNSIGNED NOT NULL,
  `category_id` INT UNSIGNED DEFAULT NULL,
  `description` TEXT         NOT NULL,
  `evidence`    VARCHAR(255) DEFAULT NULL,
  `status`      VARCHAR(20)  NOT NULL DEFAULT 'pending', -- pending | reviewing | resolved | rejected
  `admin_note`  TEXT         DEFAULT NULL,
  `resolved_at` TIMESTAMP    NULL DEFAULT NULL,
  `created_at`  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_reports_user` (`user_id`),
  KEY `idx_reports_doctor` (`doctor_id`),
  KEY `idx_reports_category` (`category_id`),
  KEY `idx_reports_status` (`status`),
  CONSTRAINT `fk_reports_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_reports_doctor`
    FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_reports_category`
    FOREIGN KEY (`category_id`) REFERENCES `report_categories` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- TABEL: admin_activity_logs
-- Riwayat aktivitas admin.
-- =====================================================================
CREATE TABLE `admin_activity_logs` (
  `id`          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `admin_id`    INT UNSIGNED DEFAULT NULL,
  `action`      VARCHAR(60)  NOT NULL,
  `target_type` VARCHAR(40)  DEFAULT NULL,
  `target_id`   INT UNSIGNED DEFAULT NULL,
  `description` VARCHAR(255) DEFAULT NULL,
  `created_at`  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_logs_admin` (`admin_id`),
  KEY `idx_logs_action` (`action`),
  KEY `idx_logs_created` (`created_at`),
  CONSTRAINT `fk_logs_admin`
    FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
