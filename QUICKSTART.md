# MarmarX - Tezkor Boshlash Qo'llanmasi

> **⚠️ Muhim:** Bu qo'llanma **lokal development** uchun. Production deployment uchun [DEPLOYMENT.md](DEPLOYMENT.md) faylini ko'ring.

## Production (Dokploy Server)

Dastur Dokploy serverida production holatida ishlayapti. Production deployment haqida to'liq ma'lumot: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Development (Lokal)

### 1. Sozlamalar

`.env` faylini yarating (`.env.example` dan nusxa oling):

```bash
cp .env.example .env
```

`.env` faylini tahrirlang va `BOT_TOKEN` ni to'ldiring:
- Telegram Bot token olish: [@BotFather](https://t.me/BotFather) ga murojaat qiling

### 2. Docker orqali ishga tushirish (Tavsiya etiladi)

```bash
# Barcha servislarni ishga tushirish
docker-compose up -d

# Loglarni kuzatish
docker-compose logs -f

# API: http://localhost:8000
# Admin Panel: http://localhost:8000/admin
# Bot: Telegram orqali /start buyrug'ini bosing
```

## 3. Admin Panel

- URL: http://localhost:8000/admin
- Username: `admin` (`.env` dan)
- Password: `admin123` (`.env` dan)

## 4. API Test Qilish

```bash
# Sog'liqni tekshirish
curl http://localhost:8000/health

# Mahsulotlarni olish
curl http://localhost:8000/products

# Narxni hisoblash (dona uchun)
curl -X POST http://localhost:8000/calculate-price \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 5}'

# Narxni hisoblash (kv_metr uchun)
curl -X POST http://localhost:8000/calculate-price \
  -H "Content-Type: application/json" \
  -d '{"product_id": 2, "area": 10.5}'
```

## 5. Botni Test Qilish

1. Telegram da botingizni toping
2. `/start` buyrug'ini yuboring
3. Web App (Mini App) orqali ma'lumot yuborsangiz, bot uni qabul qiladi va formatlangan javob qaytaradi

## 6. Ma'lumotlar Bazasiga Ma'lumot Qo'shish

Admin panel orqali:
1. http://localhost:8000/admin ga kiring
2. "Kategoriyalar" bo'limiga kiring va kategoriya qo'shing
3. "Mahsulotlar" bo'limiga kiring va mahsulot qo'shing
4. "Xizmatlar" bo'limiga kiring va xizmat qo'shing

### 7. To'xtatish

```bash
docker-compose down
```

Ma'lumotlar saqlanadi (volume orqali).

## Muammolar?

### Development (Lokal)

- **Bot ishlamayapti**: `.env` faylida `BOT_TOKEN` to'g'ri ekanligini tekshiring
- **Database ulanmayapti**: `docker-compose logs db` orqali loglarni ko'ring
- **Port band**: `docker-compose.yml` da portlarni o'zgartiring
- **Bot conflict**: Faqat bitta bot instance ishlashi kerak. Agar production bot ishlayapti, lokal botni o'chiring

### Production

Production muammolari uchun: [DEPLOYMENT.md](DEPLOYMENT.md) yoki [TROUBLESHOOTING.md](TROUBLESHOOTING.md) fayllarini ko'ring.
