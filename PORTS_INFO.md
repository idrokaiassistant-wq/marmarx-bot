# Port Sozlamalari

## O'zgartirilgan Portlar

Sizning kompyuteringizda ba'zi portlar band bo'lgani uchun, quyidagi portlar o'zgartirildi:

### Database (PostgreSQL)
- **Tashqi port (sizning kompyuteringizdan):** `5434`
- **Ichki port (konteynerlar o'rtasida):** `5432`
- **Lokal ulanish:** `localhost:5434`

### API (FastAPI)
- **Tashqi port (sizning kompyuteringizdan):** `8002`
- **Ichki port (konteyner ichida):** `8000`
- **API URL:** `http://localhost:8002`
- **Admin Panel:** `http://localhost:8002/admin`

### Bot
- Bot port talab qilmaydi (faqat Telegram orqali ishlaydi)

---

## Ulanish Ma'lumotlari

### API Endpointlar
- **Asosiy:** http://localhost:8002
- **Health Check:** http://localhost:8002/health
- **Admin Panel:** http://localhost:8002/admin
- **API Docs:** http://localhost:8002/docs

### Database (Agar lokal klient ishlatayotgan bo'lsangiz)
- **Host:** `localhost`
- **Port:** `5434`
- **User:** `marmarx`
- **Password:** `marmarx_password`
- **Database:** `marmarx_db`

---

## Muhim Eslatma

Konteynerlar o'rtasida ulanish (`api` va `bot` servislari `db` ga) **o'zgarmaydi** - ular ichki Docker tarmog'i orqali `db:5432` ga ulanadi. Faqat sizning kompyuteringizdan tashqi ulanish uchun portlar o'zgartirildi.

---

## Tekshirish

```powershell
# Konteynerlarni ko'rish
docker-compose ps

# Loglarni ko'rish
docker-compose logs -f

# API ni tekshirish
curl http://localhost:8002/health
```
