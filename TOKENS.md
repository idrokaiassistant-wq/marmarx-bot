# Tokens va Sozlamalar Ro'yxati

## .env Faylini To'ldirish

`.env` faylini yarating va quyidagi qiymatlarni to'ldiring:

### 1. Database (Ma'lumotlar Bazasi)

```env
DB_URL=postgresql+asyncpg://marmarx:marmarx_password@localhost:5432/marmarx_db
```

**Tavsif:** PostgreSQL ma'lumotlar bazasi ulanishi.

**Format:** `postgresql+asyncpg://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME`

**Lokal ishlatish uchun:**
- Username: `marmarx`
- Password: `marmarx_password`
- Host: `localhost` (lokal) yoki `db` (Docker ichida)
- Port: `5432`
- Database: `marmarx_db`

**O'zgartirish:** Agar Docker Compose ishlatayotgan bo'lsangiz, `docker-compose.yml` faylida sozlamalar mavjud.

---

### 2. Telegram Bot Token (MAJBURIY)

```env
BOT_TOKEN=your_bot_token_here
```

**Tavsif:** Telegram bot token. Bu bot ishlashi uchun zarur.

**Qanday olish:**
1. Telegram da [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting (masalan: "MarmarX Bot")
4. Bot username kiriting (masalan: "marmarx_bot" - oxirida `_bot` bo'lishi kerak)
5. BotFather sizga token beradi, shuni `.env` fayliga qo'ying

**Misol:**
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
```

**⚠️ MUHIM:** Bu tokenni hech kimga ko'rsatmang va GitHub ga yuklamang!

---

### 3. Admin Panel Sozlamalari

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

**Tavsif:** Admin panelga kirish uchun foydalanuvchi nomi va parol.

**Tavsiya:**
- Production muhitida kuchli parol ishlating
- Username va password ni o'zgartiring
- Parol kamida 8 belgidan iborat bo'lishi kerak

**Misol (Production uchun):**
```env
ADMIN_USERNAME=marmarx_admin
ADMIN_PASSWORD=KuchliParol123!@#
```

---

## To'liq .env Fayl Misoli

```env
# Database
DB_URL=postgresql+asyncpg://marmarx:marmarx_password@localhost:5432/marmarx_db

# Telegram Bot (MAJBURIY - BotFather dan oling)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890

# Admin Panel
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

---

## Qadam-baqadam Ko'rsatma

### 1-qadam: .env Faylini Yaratish

```bash
# Windows PowerShell
New-Item -Path .env -ItemType File

# Linux/Mac
touch .env
```

### 2-qadam: .env Faylini Tahrirlash

Yuqoridagi misoldan foydalanib, `.env` faylini to'ldiring.

### 3-qadam: BOT_TOKEN Olish

1. Telegram da [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` yuboring
3. Ko'rsatmalarga amal qiling
4. Olingan tokenni `.env` fayliga qo'ying

### 4-qadam: Tekshirish

```bash
# Docker Compose orqali
docker-compose up -d

# Loglarni ko'rish
docker-compose logs bot
```

Agar bot muvaffaqiyatli ishga tushgan bo'lsa, loglarda xatolik bo'lmaydi.

---

## Xavfsizlik Tavsiyalari

1. ✅ `.env` faylini `.gitignore` ga qo'shing (allaqachon qo'shilgan)
2. ✅ Production muhitida kuchli parollar ishlating
3. ✅ BOT_TOKEN ni hech kimga ko'rsatmang
4. ✅ `.env` faylini GitHub ga yuklamang
5. ✅ Production uchun alohida `.env.production` fayli yarating

---

## Muammolarni Hal Qilish

### Bot ishlamayapti
- `.env` faylida `BOT_TOKEN` mavjudligini tekshiring
- Token to'g'ri formatda ekanligini tekshiring (raqam:harflar-raqamlar)
- BotFather dan yangi token oling, agar eski token noto'g'ri bo'lsa

### Database ulanmayapti
- `DB_URL` to'g'ri formatda ekanligini tekshiring
- PostgreSQL ishga tushganligini tekshiring
- Docker Compose ishlatayotgan bo'lsangiz, `docker-compose logs db` orqali loglarni ko'ring

---

## Qo'shimcha Ma'lumot

- Docker Compose ishlatayotgan bo'lsangiz, `.env` fayl avtomatik yuklanadi
- Lokal ishlatayotgan bo'lsangiz, `python-dotenv` avtomatik `.env` faylini yuklaydi
- Sozlamalarni o'zgartirgandan keyin, servislarni qayta ishga tushiring
