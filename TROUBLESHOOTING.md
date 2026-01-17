# Template Muammosini Hal Qilish

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
