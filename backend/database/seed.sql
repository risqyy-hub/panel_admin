-- =====================================================================
-- ADMIN DOKTER - Seed Data
-- Cara pakai: mysql -u root admin_dokter < database/seed.sql
--
-- Akun login:
--   Admin : admin@admindoctor.id  / Admin123!
--   User  : budi@mail.com         / password123  (semua user & dokter)
-- Password disimpan sebagai bcrypt hash (bukan plaintext).
-- =====================================================================
USE `admin_dokter`;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE `reports`;
TRUNCATE TABLE `report_categories`;
TRUNCATE TABLE `doctor_documents`;
TRUNCATE TABLE `doctors`;
TRUNCATE TABLE `sliders`;
TRUNCATE TABLE `admin_activity_logs`;
TRUNCATE TABLE `users`;
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================================
-- KATEGORI LAPORAN (7 kategori)
-- =====================================================================
INSERT INTO `report_categories` (`id`, `name`, `description`) VALUES
(1, 'Pelayanan buruk',              'Layanan yang tidak memuaskan atau tidak sesuai standar'),
(2, 'Perilaku tidak profesional',   'Sikap dokter yang tidak profesional saat menangani pasien'),
(3, 'Informasi dokter tidak sesuai','Profil/spesialisasi dokter tidak sesuai kenyataan'),
(4, 'Dugaan penipuan',              'Dugaan penipuan atau praktik menyesatkan'),
(5, 'Pelecehan',                    'Pelecehan dalam bentuk apa pun'),
(6, 'Masalah konsultasi',           'Masalah pada proses konsultasi/muat ulang obat'),
(7, 'Lainnya',                      'Keluhan lain yang tidak termasuk kategori di atas');

-- =====================================================================
-- USERS
-- id 1      : admin
-- id 2-6    : user biasa (5 user)
-- id 7-13   : dokter (7 dokter: 3 pending, 3 approved, 1 rejected)
-- =====================================================================
INSERT INTO `users` (`id`, `name`, `email`, `password`, `phone`, `role`, `status`, `avatar`) VALUES
(1,  'Super Admin',   'admin@admindoctor.id', '$2b$12$1zPWET34QY8i4fkF1O7TT.oXF7wDNbKbbP2mRGGK9/IkPzP7N4Iiy', '081100000001', 'admin',  'active',  NULL),

(2,  'Budi Santoso',  'budi@mail.com',        '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081200000001', 'user',   'active',  NULL),
(3,  'Siti Aminah',   'siti@mail.com',        '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081200000002', 'user',   'active',  NULL),
(4,  'Andi Wijaya',   'andi@mail.com',        '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081200000003', 'user',   'active',  NULL),
(5,  'Dewi Lestari',  'dewi@mail.com',        '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081200000004', 'user',   'active',  NULL),
(6,  'Rudi Hartono',  'rudi@mail.com',        '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081200000005', 'user',   'suspended', NULL),

(7,  'dr. Agus Prasetyo, Sp.PD',  'agus@mail.com',  '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081300000001', 'doctor', 'active', NULL),
(8,  'dr. Bella Kartika, Sp.A',   'bella@mail.com', '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081300000002', 'doctor', 'active', NULL),
(9,  'dr. Citra Dewi, Sp.KG',     'citra@mail.com', '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081300000003', 'doctor', 'active', NULL),
(10, 'dr. Dimas Putra, Sp.JP',    'dimas@mail.com', '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081300000004', 'doctor', 'active', NULL),
(11, 'dr. Eka Rahayu, Sp.THT',    'eka@mail.com',   '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081300000005', 'doctor', 'active', NULL),
(12, 'dr. Fajar Nugroho, Sp.M',   'fajar@mail.com', '$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081300000006', 'doctor', 'active', NULL),
(13, 'dr. Gilang Ramadhan',       'gilang@mail.com','$2b$12$SfVbWxl7sjMRs86QPKaF4uz.QAfb3JuJrzLto/6XnBCKs2N/Py5WO', '081300000007', 'doctor', 'active', NULL);

-- =====================================================================
-- DOCTORS
-- approved : 7, 8, 9
-- pending  : 10, 11, 12
-- rejected : 13
-- =====================================================================
INSERT INTO `doctors` (`id`, `user_id`, `specialization`, `license_number`, `education`, `experience`, `bio`, `verification_status`, `rejection_reason`, `verified_at`, `is_active`) VALUES
(1, 7,  'Penyakit Dalam',   'STR-1234567890', 'Universitas Indonesia, Sp.PD', '12 tahun', 'Dokter spesialis penyakit dalam dengan fokus pada penyakit metabolik.', 'approved', NULL, '2026-08-10 09:00:00', 1),
(2, 8,  'Anak',             'STR-2234567890', 'Universitas Gadjah Mada, Sp.A', '9 tahun',  'Dokter spesialis anak, konsultasi tumbuh kembang dan imunisasi.',        'approved', NULL, '2026-08-12 10:30:00', 1),
(3, 9,  'Kardiologi',       'STR-3234567890', 'Universitas Airlangga, Sp.JP',  '15 tahun', 'Dokter spesialis jantung dan pembuluh darah.',                            'approved', NULL, '2026-08-15 08:15:00', 1),
(4, 10, 'Jantung',          'STR-4234567890', 'Universitas Diponegoro, Sp.JP',  '6 tahun',  'Dokter spesialis jantung, menangani gagal jantung dan aritmia.',          'pending',  NULL, NULL, 1),
(5, 11, 'THT',              'STR-5234567890', 'Universitas Brawijaya, Sp.THT',  '7 tahun',  'Dokter spesialis THT-KL, layanan konsultasi telinga, hidung, tenggorokan.','pending', NULL, NULL, 1),
(6, 12, 'Mata',             'STR-6234567890', 'Universitas Hasanuddin, Sp.M',   '5 tahun',  'Dokter spesialis mata, pemeriksaan refraksi dan katarak.',                'pending',  NULL, NULL, 1),
(7, 13, 'Umum',             'SIP-7234567890', 'Universitas Sriwijaya, dr.',     '3 tahun',  'Dokter umum praktek.',                                                    'rejected', 'Nomor SIP tidak dapat diverifikasi dan dokumen ijazah tidak terbaca.', '2026-09-01 14:00:00', 0);

-- =====================================================================
-- DOKUMEN PENDUKUNG DOKTER
-- =====================================================================
INSERT INTO `doctor_documents` (`doctor_id`, `document_type`, `document_path`, `verification_status`) VALUES
(1, 'str',      '/uploads/documents/str_agus.pdf',  'approved'),
(1, 'sip',      '/uploads/documents/sip_agus.pdf',  'approved'),
(2, 'str',      '/uploads/documents/str_bella.pdf', 'approved'),
(2, 'ijazah',   '/uploads/documents/ijazah_bella.pdf', 'approved'),
(3, 'str',      '/uploads/documents/str_citra.pdf', 'approved'),
(4, 'str',      '/uploads/documents/str_dimas.pdf', 'pending'),
(5, 'str',      '/uploads/documents/str_eka.pdf',   'pending'),
(6, 'sertifikat','/uploads/documents/sertifikat_fajar.pdf', 'pending'),
(7, 'str',      '/uploads/documents/str_gilang.pdf','rejected');

-- =====================================================================
-- SLIDERS (3 banner)
-- =====================================================================
INSERT INTO `sliders` (`title`, `description`, `image`, `link`, `sort_order`, `status`) VALUES
('Konsultasi Dokter Online', 'Hubungi dokter spesialis kapan saja melalui chat dan video call.', '/uploads/sliders/konsultasi-online.jpg', '/doctors',      1, 'active'),
('Cek Kesehatan Gratis',     'Program pemeriksaan kesehatan gratis setiap bulan di klinik partner.', '/uploads/sliders/cek-kesehatan.jpg',    '/reports',     2, 'active'),
('Promo Kesehatan Mental',   'Diskon 30% sesi konsultasi psikolog selama bulan Oktober.',           '/uploads/sliders/promo-mental.jpg',     '/settings',    3, 'inactive');

-- =====================================================================
-- LAPORAN (5 laporan)
-- =====================================================================
INSERT INTO `reports` (`user_id`, `doctor_id`, `category_id`, `description`, `evidence`, `status`, `admin_note`, `resolved_at`) VALUES
(2, 1, 1, 'Menunggu lebih dari 45 menit padahal sudah janji jam 10.00.', NULL,                                              'pending',   NULL, NULL),
(3, 1, 6, 'Resep obat tidak dijawab selama 3 hari setelah konsultasi.', '/uploads/evidence/chat-3-hari.png',              'reviewing', 'Sedang dikonfirmasi ke dokter terkait.', NULL),
(4, 2, 2, 'Dokter terdengar kasar saat menjelaskan hasil pemeriksaan anak.', NULL,                                         'resolved',  'Dokter telah diberi teguran dan meminta maaf.', '2026-09-20 11:00:00'),
(5, 3, 3, 'Profil menyebut Sp.JP padahal saat konsultasi diarahkan ke dokter umum.', NULL,                                'rejected',  'Tidak ditemukan bukti ketidaksesuaian pada sistem.', '2026-09-22 15:30:00'),
(6, 7, 4, 'Minta biaya konsultasi transfer ke rekening pribadi di luar aplikasi.', '/uploads/evidence/bukti-transfer.jpg','pending',   NULL, NULL);

-- =====================================================================
-- LOG AKTIVITAS ADMIN
-- =====================================================================
INSERT INTO `admin_activity_logs` (`admin_id`, `action`, `target_type`, `target_id`, `description`) VALUES
(1, 'login',                'user',  1,    'Admin login ke panel admin'),
(1, 'approve_doctor',       'doctor',1,    'Menyetujui verifikasi dr. Agus Prasetyo, Sp.PD'),
(1, 'approve_doctor',       'doctor',2,    'Menyetujui verifikasi dr. Bella Kartika, Sp.A'),
(1, 'approve_doctor',       'doctor',3,    'Menyetujui verifikasi dr. Citra Dewi, Sp.KG'),
(1, 'reject_doctor',        'doctor',7,    'Menolak pendaftaran dr. Gilang Ramadhan'),
(1, 'suspend_user',         'user',  6,    'Menonaktifkan akun Rudi Hartono'),
(1, 'create_slider',        'slider',1,    'Membuat slider Konsultasi Dokter Online'),
(1, 'update_report_status', 'report',2,    'Mengubah status laporan #2 menjadi reviewing'),
(1, 'update_report_status', 'report',4,    'Mengubah status laporan #4 menjadi rejected'),
(1, 'deactivate_slider',    'slider',3,    'Menonaktifkan slider Promo Kesehatan Mental');
