# Dokploy'da Admin Panel Sozlash (Telegram Bot)

## ADMIN_USER_IDS Qo'shish

Telegram botda admin paneldan foydalanish uchun `ADMIN_USER_IDS` environment variable'ni qo'shish kerak.

### Qadam 1: User ID'ni Olish

Telegram user ID'ni olish uchun:

1. Telegram'da [@userinfobot](https://t.me/userinfobot) ga murojaat qiling
2. `/start` yuboring
3. Bot sizga user ID'ni ko'rsatadi (masalan: `924016177`)

### Qadam 2: Dokploy'da Environment Variable Qo'shish

1. **Dokploy Dashboard'ga kiring**
   - URL: `http://194.164.72.8:3000`

2. **marmarx-bot Servisiga O'ting**
   - Projects > MarmarX > production
   - `marmarx-bot` servisini tanlang

3. **Environment Tab'ga O'ting**
   - Servis sahifasida "Environment" tab'ini bosing

4. **Environment Settings Bo'limida:**
   - "Environment Settings" bo'limiga o'ting
   - Mavjud environment variable'larni ko'ring (ko'z ikonka bilan ko'rish mumkin)

5. **Yangi Variable Qo'shish:**
   - Environment variable'lar ro'yxatiga qo'shing:
   ```
   ADMIN_USER_IDS=924016177
   ```
   
   **Agar bir nechta admin bo'lsa:**
   ```
   ADMIN_USER_IDS=924016177,123456789,987654321
   ```
   (Vergul bilan ajratilgan user ID'lar)

6. **Saqlash:**
   - "Save" yoki "Update" tugmasini bosing

### Qadam 3: Servisni Restart Qilish

Environment variable qo'shilgandan keyin:

1. `marmarx-bot` servisini **Restart** qiling
   - Servis sahifasida "Restart" tugmasini bosing
   - Yoki terminal orqali: servis avtomatik qayta yuklanishi mumkin

2. **Tekshirish:**
   - Bot loglarini ko'ring
   - Telegram'da `/admin` yuboring
   - Admin panel ochilishi kerak

## To'liq Environment Variables (marmarx-bot uchun)

`marmarx-bot` servisida quyidagi environment variable'lar bo'lishi kerak:

```env
DB_URL=postgresql+asyncpg://marmarx:marmarx_password@marmarx-db:5432/marmarx_db
BOT_TOKEN=<your_bot_token>
ADMIN_USER_IDS=924016177
```

## Qaysi Servisga Qo'shish Kerak?

### ✅ marmarx-bot
**Qo'shish kerak:**
- `ADMIN_USER_IDS` - Telegram bot admin funksiyasi uchun
- `BOT_TOKEN` - Telegram bot token
- `DB_URL` - Database ulanishi

### ❌ marmarx-api
**Qo'shish kerak emas:**
- Web admin panel uchun `ADMIN_USERNAME` va `ADMIN_PASSWORD` ishlatiladi
- `ADMIN_USER_IDS` bu servisda ishlatilmaydi

## Admin Panel Funksiyalari

Admin user ID qo'shilgandan keyin:

1. **Telegram'da:**
   - `/admin` - Admin panel menyusi
   - "🔧 Admin Panel" tugmasi (asosiy menyuda)

2. **Mumkin bo'lgan ishlar:**
   - ✅ Mahsulot qo'shish
   - ✅ Kategoriya qo'shish
   - ✅ Buyurtmalarni ko'rish (kelajakda)
   - ✅ Mahsulotlarni tahrirlash/o'chirish (kelajakda)

## Muammolarni Hal Qilish

### Admin panel ochilmayapti

1. **User ID to'g'ri ekanligini tekshiring:**
   - `@userinfobot` orqali user ID'ni qayta tekshiring
   - `ADMIN_USER_IDS` da to'g'ri formatda ekanligini tekshiring

2. **Environment variable saqlangannimi:**
   - Dokploy'da "Save" tugmasini bosganmisiz?
   - Servis restart qilganmisiz?

3. **Loglarni tekshiring:**
   - Dokploy > marmarx-bot > Logs
   - Xato xabarlarini ko'ring

### Bir nechta admin qo'shish

Agar bir nechta foydalanuvchini admin qilmoqchi bo'lsangiz:

```env
ADMIN_USER_IDS=924016177,123456789,987654321
```

**Format:**
- Vergul bilan ajratilgan
- Bo'sh joy yo'q
- Faqat raqamlar

## Misol

1. User ID: `924016177` (sizning ID'ingiz)

2. Dokploy'da `marmarx-bot` servisining Environment Settings'ga qo'shing:
   ```
   ADMIN_USER_IDS=924016177
   ```

3. Servisni restart qiling

4. Telegram'da `/admin` yuboring

5. Admin panel ochiladi! 🎉

## Xavfsizlik

⚠️ **Muhim:**
- `ADMIN_USER_IDS` faqat ishonchli foydalanuvchilarga berilishi kerak
- User ID'larni hech kimga ko'rsatmang
- Production'da faqat kerakli odamlarga admin huquqi bering
