# ADMIN DOKTER

Admin panel untuk mengelola aplikasi dokter. Full-stack terpisah:

| Layer    | Teknologi                                       |
| -------- | ----------------------------------------------- |
| Frontend | Next.js 16 + TypeScript + App Router + Tailwind CSS |
| Backend  | Python + FastAPI + SQLAlchemy                   |
| Database | MariaDB/MySQL (`admin_dokter`)                  |

## Struktur Project

```
admin-dokter/
├── frontend/          # Next.js (http://localhost:3000)
│   ├── app/           # Halaman App Router
│   ├── components/    # Komponen reusable
│   ├── lib/           # API client, auth, utils
│   ├── types/         # Tipe TypeScript
│   └── proxy.ts       # Proteksi rute admin
└── backend/           # FastAPI (http://127.0.0.1:8000)
    ├── app/
    │   ├── api/       # Router endpoint
    │   ├── core/      # config, database, security
    │   ├── models/    # Model ORM
    │   ├── schemas/   # Skema Pydantic
    │   ├── services/  # Logika bisnis
    │   └── utils/     # Helper response/pagination/upload
    ├── database/      # schema.sql + seed.sql
    ├── .env           # Konfigurasi rahasia (tidak di-commit)
    └── requirements.txt
```

## Prasyarat

- Node.js 20.9+ (dites dengan v22)
- Python 3.11+ (dites dengan 3.14)
- MariaDB/MySQL berjalan (mis. XAMPP, port 3306)

## CARA MENJALANKAN

### 1. Database

```powershell
# Buat tabel
cmd /c '"C:\xampp\mysql\bin\mysql.exe" -u root < backend\database\schema.sql'

# Isi data awal (admin, user, dokter, slider, laporan)
cmd /c '"C:\xampp\mysql\bin\mysql.exe" -u root admin_dokter < backend\database\seed.sql'
```

### 2. Backend (FastAPI)

```powershell
cd backend

# Buat virtual environment (sekali saja)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Jalankan server
fastapi dev app/main.py
# atau: .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

API: <http://127.0.0.1:8000> · Docs: <http://127.0.0.1:8000/docs>

### 3. Frontend (Next.js)

```powershell
cd frontend
npm install
npm run dev
```

Admin Panel: <http://localhost:3000>

## AKUN LOGIN ADMIN

| Field  | Value                   |
| ------ | ----------------------- |
| Email  | `admin@admindoctor.id`  |
| Password | `Admin123!`           |

Akun lain (user/dokter): password `password123`
(contoh: `budi@mail.com`, `agus@mail.com`).

## FITUR ADMIN

1. Login/Logout admin (JWT + role check)
2. Dashboard statistik (data real dari database)
3. Verifikasi dokter (setujui / tolak dengan alasan)
4. Aktifkan & nonaktifkan akun dokter
5. Kelola user (search, filter, pagination, hapus dengan konfirmasi)
6. Kelola slider (CRUD + upload gambar aman)
7. Laporan user → dokter (detail, ubah status, catatan admin)
8. Semua endpoint admin dilindungi `require_admin`

## API ENDPOINTS

Semua endpoint (kecuali login) membutuhkan header:
`Authorization: Bearer <token>`

| Method | Endpoint | Deskripsi |
| ------ | -------- | --------- |
| POST | `/api/auth/login` | Login |
| GET | `/api/auth/me` | Profil dari token |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/dashboard/stats` | Statistik |
| GET | `/api/dashboard/recent-doctors` | Dokter terbaru |
| GET | `/api/dashboard/recent-reports` | Laporan terbaru |
| GET | `/api/dashboard/recent-activities` | Aktivitas terbaru |
| GET | `/api/doctors?page&limit&search&status` | List dokter |
| GET | `/api/doctors/{id}` | Detail dokter |
| PUT | `/api/doctors/{id}/approve` | Setujui dokter |
| PUT | `/api/doctors/{id}/reject` | Tolak (body: `reason`) |
| PUT | `/api/doctors/{id}/activate` | Aktifkan |
| PUT | `/api/doctors/{id}/deactivate` | Nonaktifkan |
| GET | `/api/users?page&limit&search&status` | List user |
| GET | `/api/users/{id}` | Detail user |
| PUT | `/api/users/{id}/activate` | Aktifkan |
| PUT | `/api/users/{id}/deactivate` | Nonaktifkan |
| DELETE | `/api/users/{id}` | Hapus user |
| GET | `/api/sliders` | List slider |
| GET | `/api/sliders/{id}` | Detail slider |
| POST | `/api/sliders` | Buat (multipart) |
| PUT | `/api/sliders/{id}` | Edit (multipart) |
| DELETE | `/api/sliders/{id}` | Hapus |
| PUT | `/api/sliders/{id}/activate` | Aktifkan |
| PUT | `/api/sliders/{id}/deactivate` | Nonaktifkan |
| GET | `/api/reports?page&limit&search&status` | List laporan |
| GET | `/api/reports/categories` | Kategori laporan |
| GET | `/api/reports/{id}` | Detail laporan |
| PUT | `/api/reports/{id}/status` | Ubah status + catatan |

Format response sukses:
`{"success": true, "message": "...", "data": {...}}`
List menambahkan: `"pagination": {"page", "limit", "total", "total_pages"}`
Format error: `{"success": false, "message": "..."}`

## KEAMANAN

- Password di-hash dengan bcrypt (tidak pernah plaintext)
- JWT secret & DATABASE_URL di `.env` (tidak di-commit)
- Otorisasi backend: dependency `require_admin` di semua endpoint admin
- CORS dibatasi ke `http://localhost:3000` (bukan `*`)
- Upload gambar: validasi MIME (JPG/PNG/WEBP/GIF) + maks 5 MB + nama file acak
- Query menggunakan SQLAlchemy ORM (parameterized - anti SQL injection)

## MENAMBAH ADMIN BARU

Login ke database lalu insert (password harus bcrypt hash):

```sql
USE admin_dokter;
-- Ganti HASH_DENGAN_HASH_BCRYPT (generate: python -c "import bcrypt; print(bcrypt.hashpw(b'password', bcrypt.gensalt(rounds=12)).decode())")
INSERT INTO users (name, email, password, phone, role, status)
VALUES ('Admin Baru', 'baru@admindoctor.id', 'HASH_DENGAN_HASH_BCRYPT', '081234567890', 'admin', 'active');
```
