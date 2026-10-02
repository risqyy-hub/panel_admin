# Backend ADMIN DOKTER (FastAPI)

REST API untuk admin panel aplikasi dokter.

## Menjalankan

```powershell
cd backend

# Pertama kali
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Setiap kali
.\.venv\Scripts\Activate.ps1
fastapi dev app/main.py
```

- API: <http://127.0.0.1:8000>
- Docs (Swagger): <http://127.0.0.1:8000/docs>

## Konfigurasi (.env)

Salin `.env.example` menjadi `.env` lalu sesuaikan:

```
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/admin_dokter
JWT_SECRET=<secret random>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## Database

```powershell
cmd /c '"C:\xampp\mysql\bin\mysql.exe" -u root < database\schema.sql'
cmd /c '"C:\xampp\mysql\bin\mysql.exe" -u root admin_dokter < database\seed.sql'
```

## Struktur

```
app/
├── main.py          # Entry point, CORS, exception handler, static files
├── core/
│   ├── config.py    # Settings dari .env
│   ├── database.py  # Engine, Session, get_db
│   └── security.py  # bcrypt, JWT, get_current_user, require_admin
├── models/          # ORM (users, doctors, sliders, reports, ...)
├── schemas/         # Validasi Pydantic
├── api/             # Router endpoint
├── services/        # Logika bisnis
└── utils/           # response, pagination, activity log, storage
```

## Testing cepat

```powershell
# Login
$r = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login" -Method Post -ContentType "application/json" -Body '{"email":"admin@admindoctor.id","password":"Admin123!"}'

# Pakai token
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/dashboard/stats" -Headers @{Authorization="Bearer $($r.data.access_token)"}
```
