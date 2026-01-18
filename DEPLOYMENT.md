# MarmarX - Production Deployment (Dokploy)

## Umumiy Ma'lumot

MarmarX dasturi **Dokploy platformasi** orqali production serverda ishlayapti. Docker **shart emas** - dastur Dokploy serverida to'g'ridan-to'g'ri ishlaydi.

> **⚠️ Muhim:** Docker va `docker-compose.yml` faqat lokal development uchun ishlatiladi. Production deployment Dokploy orqali boshqariladi.

## Server Ma'lumotlari

- **Platforma:** Dokploy (Hostinger VPS)
- **Server IP:** `194.164.72.8`
- **OS:** Ubuntu 24.04
- **Environment:** Production

## Production Servislar

Dokploy dashboard'da quyidagi servislar ishlayapti:

### 1. marmarx-api
- **Type:** Web Service
- **Image/Command:** FastAPI backend
- **Status:** ✅ Active
- **Endpoint:** API va Admin Panel

### 2. marmarx-bot
- **Type:** Web Service
- **Image/Command:** Aiogram Telegram bot
- **Status:** ✅ Active
- **Function:** Telegram bot polling

### 3. marmarx-db
- **Type:** PostgreSQL Database
- **Status:** ✅ Active
- **Function:** Ma'lumotlar bazasi

### 4. marmarx-frontend
- **Type:** Web Service
- **Image/Command:** Nginx static files
- **Status:** ✅ Active
- **Function:** Frontend sahifalari

## Environment Variables (Production)

Production environment'da quyidagi environment variables sozlangan:

```env
# marmarx-bot servisi uchun:
DB_URL=postgresql+asyncpg://marmarx:marmarx_password@marmarx-db:5432/marmarx_db
BOT_TOKEN=<production_bot_token>
ADMIN_USER_IDS=<telegram_user_id1>,<telegram_user_id2>  # Vergul bilan ajratilgan

# marmarx-api servisi uchun (web admin panel):
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<production_admin_password>
```

> **Eslatma:** Aniq qiymatlar Dokploy dashboard'da environment variables bo'limida saqlanadi.

## Loglarni Ko'rish

Dokploy dashboard orqali loglarni ko'rish:

1. Dokploy dashboard'ga kiring
2. **Projects > MarmarX > production** ga o'ting
3. Kerakli servisni tanlang
4. **Logs** bo'limini oching

### Log Format

Bot servisi loglarida quyidagilar ko'rinadi:
```
- Database initialized
- Starting bot...
- Start polling
- Run polling for bot @MarmarX_bot
- Update handled...
```

## Monitoring

### Servislar Holatini Tekshirish

Dokploy dashboard'da:
- Har bir servis **yashil nuqta** bilan belgilangan (Active)
- Servislar yaratilgan vaqt ko'rsatilgan
- Real-time status monitoring mavjud

### API Health Check

Production API health check:
```bash
curl https://<your-api-domain>/health
```

Yoki Dokploy dashboard orqali:
- API servisining logs bo'limida health check natijalari ko'rinadi

## Admin Panel

Production Admin Panel:
- Dokploy dashboard orqali API URL'dan `/admin` endpointiga kirish
- Credentials: Dokploy environment variables'da saqlangan

## Bot Testing

Production botini test qilish:
1. Telegram'da `@MarmarX_bot` ga murojaat qiling
2. `/start` buyrug'ini yuboring
3. Bot javob berishi kerak

> **Eslatma:** Bot conflict xatosi bo'lishi mumkin agar lokal development bot ham ishlayotgan bo'lsa. Production bot faqat Dokploy serverida ishlaydi.

## Ma'lumotlar Bazasi

Production database:
- **Host:** `marmarx-db` (Dokploy service name)
- **Port:** `5432` (ichki Docker tarmog'i)
- **Database:** `marmarx_db`
- **User:** `marmarx`
- **Password:** Dokploy environment variables'da saqlangan

> **Eslatma:** Database faqat Dokploy ichki tarmog'i orqali ulanish mumkin.

## Update Qilish (Yangilash)

Kod yangilanishini deploy qilish:

1. Git repository'ni yangilash
2. Dokploy dashboard'da servislarni **Restart** qilish
   - Yoki **Redeploy** buyrug'ini ishlatish

> **Eslatma:** Dokploy avtomatik ravishda yangi kodni deploy qilishi mumkin (Git integration sozlangani bo'lsa).

## Xavfsizlik

### Environment Variables
- Barcha sensitive ma'lumotlar Dokploy environment variables'da saqlanadi
- `.env` fayl Git'ga commit qilinmaydi (`.gitignore` da)

### Database
- Database faqat ichki Dokploy tarmog'i orqali ulanish mumkin
- Tashqi ulanish mavjud emas (xavfsizlik uchun)

### Admin Panel
- Session-based authentication
- Admin username/password environment variables'da

## Troubleshooting

### Bot ishlamayapti
1. Dokploy dashboard'da `marmarx-bot` servisining loglarini tekshiring
2. `BOT_TOKEN` to'g'ri ekanligini tekshiring
3. Bot conflict xatosini tekshiring (faqat bitta instance ishlashi kerak)

### Database ulanmayapti
1. `marmarx-db` servisining holatini tekshiring (Active bo'lishi kerak)
2. `DB_URL` environment variable'ni tekshiring
3. Database servisi loglarini ko'ring

### API ishlamayapti
1. `marmarx-api` servisining loglarini tekshiring
2. API health check endpoint'ini test qiling
3. Database ulanishini tekshiring

### Frontend ishlamayapti
1. `marmarx-frontend` servisining holatini tekshiring
2. Nginx loglarini ko'ring
3. Static fayllar to'g'ri joylanganligini tekshiring

## Yordam

Muammolar bo'lsa:
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Batafsil muammolarni hal qilish
- Dokploy dashboard loglari - Real-time error tracking
- [README.md](README.md) - Umumiy ma'lumot

## Development va Production Farqi

| Xususiyat | Development (Lokal) | Production (Dokploy) |
|-----------|---------------------|---------------------|
| Deployment | Docker Compose | Dokploy Platform |
| Database | `localhost:5434` | `marmarx-db:5432` (ichki) |
| API URL | `http://localhost:8002` | Dokploy API domain |
| Admin Panel | `http://localhost:8002/admin` | Dokploy API domain + `/admin` |
| Bot | Lokal instance | Dokploy server instance |
| Environment | `.env` fayl | Dokploy Environment Variables |
| Logs | `docker-compose logs` | Dokploy Dashboard Logs |

> **⚠️ Muhim:** Development va production botlar bir vaqtda ishlamaydi (Telegram conflict). Production bot ishlayotgan bo'lsa, lokal botni o'chiring.
