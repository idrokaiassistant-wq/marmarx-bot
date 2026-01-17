# .env Faylini Sozlash - Qisqa Ko'rsatma

## ⚠️ MAJBURIY: BOT_TOKEN Olish

Bot ishlashi uchun Telegram Bot Token kerak:

1. Telegram da [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting
4. Bot username kiriting (oxirida `_bot` bo'lishi kerak)
5. Olingan tokenni `.env` faylida `BOT_TOKEN` ga qo'ying

**Misol token:** `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890`

---

## .env Fayl Tarkibi

```env
# Database - O'zgartirish shart emas (Docker Compose uchun)
DB_URL=postgresql+asyncpg://marmarx:marmarx_password@localhost:5432/marmarx_db

# Telegram Bot - ⚠️ MAJBURIY TO'LDIRISH KERAK!
BOT_TOKEN=your_bot_token_here

# Admin Panel - Xohlasangiz o'zgartiring
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

---

## Tezkor Boshlash

1. `.env` faylini oching
2. `BOT_TOKEN=your_bot_token_here` ni o'zgartiring va BotFather dan olingan tokenni qo'ying
3. Saqlang
4. `docker-compose up -d` buyrug'ini ishga tushiring

---

Batafsil ma'lumot uchun `TOKENS.md` faylini ko'ring.
