# Bot Conflict Muammosini Hal Qilish

## ✅ Holat: Mahalliy Bot O'chgan

Tekshiruv natijalari ko'rsatdiki:
- ✅ Docker konteynerlar o'chgan (Exited)
- ✅ Python jarayonlari ishlamayapti
- ✅ Mahalliy bot ishlamayapti

## 📋 Keyingi Qadamlar

### 1. Serverdagi bot holatini tekshirish

1. **Dokploy** ga kiring
2. `marmarx-bot` servisiga o'ting
3. **Logs** bo'limini oching

**Kutilgan natija:**
- ✅ "Connection established" xabarlari chiqishi kerak
- ✅ "Conflict" xatosi chiqmasligi kerak
- ✅ Bot tinch ishlashi kerak

### 2. Agar hali ham "Conflict" chiqayotgan bo'lsa

**Serverdagi botni qayta ishga tushiring:**

1. Dokploy'da `marmarx-bot` servisida **Stop** tugmasini bosing
2. 5-10 soniya kutib turing
3. **Start** tugmasini bosing
4. Loglarni kuzatib turing

### 3. Botni test qilish

Telegram'da botingizga o'ting va `/start` yuboring.

**Kutilgan natija:**
- Bot javob berishi kerak
- Hech qanday xato bo'lmasligi kerak

## 🛑 Keyinchalik muammoni oldini olish

### Development (Test) vaqtida:

Agar kodni o'zgartirib test qilmoqchi bo'lsangiz:

1. **Serverdagi botni to'xtating** (Dokploy'da Stop)
2. **Mahalliy botni ishga tushiring:**
   ```bash
   docker-compose up bot
   ```
   yoki
   ```bash
   python -m app.bot.main
   ```
3. Testlarni bajaring
4. Ishingiz bitgach:
   - Mahalliy botni to'xtating (`Ctrl+C`)
   - Serverdagi botni yana yoqing (Dokploy'da Start)

### Production vaqtida:

- Faqat **serverdagi bot** ishlashi kerak
- Mahalliy kompyuterdagi Docker'ni yopib qo'ying

## 📝 Xulosa

**Hozirgi holat:** ✅ Mahalliy bot o'chgan, serverdagi bot ishlashi kerak.

**Tekshirish:** Dokploy loglarini ko'rib, conflict xatosi chiqmayotganini tasdiqlang.

**Keyinchalik:** Bir vaqtning o'zida faqat bitta bot ishlashi kerak!
