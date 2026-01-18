# Muammolarni Hal Qilish - MarmarX Bot

## 🔴 Bot Conflict Muammosi (TelegramConflictError)

### Muammo belgilari:
```
TelegramConflictError: Conflict: terminated by other getUpdates request; 
make sure that only one bot instance is running
```

### Muammoning sababi:
Telegram bitta bot token bilan faqat bitta bot instance ishlashiga ruxsat beradi. Agar bot bir vaqtning o'zida ikki joyda ishlab turgan bo'lsa (masalan, serverda va mahalliy kompyuteringizda), bu conflict xatosi paydo bo'ladi.

### ✅ Yechim:

#### 1-qadam: Mahalliy kompyuterdagi botni tekshirish

**Docker konteynerlarni tekshirish:**
```bash
docker ps -a | findstr marmarx
```

Agar konteynerlar ishlab turgan bo'lsa:
```bash
docker stop marmarx_bot
```

**Python jarayonlarini tekshirish:**
```bash
# Windows:
tasklist | findstr python

# Linux/Mac:
ps aux | grep python
```

Agar Python jarayonlari ishlab turgan bo'lsa, uni to'xtating:
- VS Code terminalida `Ctrl+C` bosing
- Yoki jarayonni to'xtating

#### 2-qadam: Docker Desktop tekshirish

Agar Docker Desktop ishlamayotgan bo'lsa (xato: `failed to connect to docker API`), demak mahalliy bot allaqachon o'chgan. 

**Tasdiqlash:**
```bash
docker ps
```

Agar xato chiqsa - Docker o'chiq, mahalliy bot ishlamayapti ✅

#### 3-qadam: Serverdagi bot holatini tekshirish

1. Dokploy (yoki boshqa server) ga kiring
2. `marmarx-bot` servisining **Logs** bo'limini oching
3. Endi conflict xatosi chiqmasligi kerak
4. Agar hali ham chiqayotgan bo'lsa, servisni qayta ishga tushiring:
   - **Stop** tugmasini bosing
   - 5-10 soniya kutib turing
   - **Start** tugmasini bosing

### 📝 Xulosa:
- **Production (Server)**: Serverdagi bot 24/7 ishlaydi
- **Development (Local)**: Mahalliy testlar uchun serverdagi botni vaqtincha to'xtatib qo'ying
- **Muammo**: Ikki botni bir vaqtning o'zida ishlatish mumkin emas

---

## 📄 Template Muammosini Hal Qilish

## Tekshirishlar

1. **Template fayllari to'g'ri joydamu?**
   ```bash
   docker-compose exec api ls -la /app/app/templates/sqladmin/
   ```
   - `list.html` va `layout.html` bo'lishi kerak

2. **API kodida `templates_dir` parametri to'g'rimi?**
   ```python
   admin = Admin(
       app, 
       engine, 
       authentication_backend=authentication_backend, 
       title="MarmarX Admin Panel",
       templates_dir="app/templates"  # ← Bu to'g'ri
   )
   ```

3. **Template'larda o'zbekcha matnlar bormi?**
   ```bash
   docker-compose exec api grep -n "Yuklab olish\|Qidirish\|Yangi\|Amallar" /app/app/templates/sqladmin/list.html
   docker-compose exec api grep -n "Chiqish" /app/app/templates/sqladmin/layout.html
   ```

4. **Browser cache muammosi?**
   - Browser'da `Ctrl+Shift+R` (yoki `Cmd+Shift+R` Mac'da) bosing - hard refresh
   - Yoki browser'da Developer Tools ochib, "Disable cache" ni yoqing

5. **API qayta ishga tushirildimi?**
   ```bash
   docker-compose restart api
   ```

## Agar hali ham ishlamasa

1. **Template'larni to'liq tekshiring:**
   ```bash
   docker-compose exec api cat /app/app/templates/sqladmin/list.html
   ```

2. **SQLAdmin loglarini tekshiring:**
   ```bash
   docker-compose logs api | grep -i template
   ```

3. **Browser console'da xatolarni tekshiring:**
   - F12 bosing
   - Console tab'ni oching
   - Xatolarni ko'ring

## Muammo hal qilinmagan bo'lsa

Template'larni to'liq qayta yozish kerak bo'lishi mumkin. SQLAdmin'ning template loader'i ba'zida cache qilishi mumkin.
