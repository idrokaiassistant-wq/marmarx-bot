# Port Muammosi Hal Qilindi

## Muammo
Port 5432 allaqachon ishlatilmoqda (mavjud PostgreSQL xizmati yoki boshqa konteyner).

## Yechim
`docker-compose.yml` faylida tashqi port `5434` ga o'zgartirildi (5432 va 5433 ham band edi).

**O'zgarish:**
- Tashqi port (host): `5434` 
- Ichki port (container): `5432` (o'zgarmaydi)

## Endi Ishlatish

### 1. Mavjud konteynerlarni to'xtatish
```powershell
docker-compose down
```

### 2. Qayta ishga tushirish
```powershell
docker-compose up -d
```

### 3. Lokal ulanish (agar kerak bo'lsa)
Agar sizda lokal PostgreSQL klienti bo'lsa va Docker konteyneriga ulanishni xohlasangiz:
- Host: `localhost`
- Port: `5434` (5432 emas!)
- User: `marmarx`
- Password: `marmarx_password`
- Database: `marmarx_db`

## Muhim Eslatma
- Konteynerlar o'rtasida ulanish (`api` va `bot` servislari `db` ga) **o'zgarmaydi** - ular `db:5432` orqali ulanadi (ichki tarmoq)
- Faqat tashqi ulanish (sizning kompyuteringizdan) `5433` port orqali bo'ladi

## Status
✅ Port 5434 bo'sh va ishlatilmoqda. Barcha eski konteynerlar va volumelar tozalandi.
