# Template Muammosi va Yechim

## Muammo
SQLAdmin template'larni qidirish tartibi:
1. Avval `templates_dir` parametri bilan belgilangan papkada qidiradi
2. Keyin default `sqladmin/templates/` papkasida qidiradi

Bizning holatda:
- `templates_dir="app/templates"` 
- SQLAdmin `app/templates/sqladmin/list.html` ni topadi ✅
- Lekin template ichida `{% extends "sqladmin/list.html" %}` yozilgan
- Bu SQLAdmin'ning default template'ini extend qilish kerak, lekin SQLAdmin avval bizning template'imizni topadi
- Natijada template o'z-o'zini extend qiladi (infinite loop)

## Yechim
Template'larni to'g'ri extend qilish kerak. SQLAdmin template'larni qidirishda:
- `sqladmin/list.html` deb yozilganda, SQLAdmin avval `templates_dir/sqladmin/list.html` ni qidiradi
- Agar topilmasa, default `sqladmin/templates/sqladmin/list.html` ni qidiradi

Bizning template'imiz `app/templates/sqladmin/list.html` da, shuning uchun u o'z-o'zini extend qiladi.

**Yechim:** Template ichida original template'ni extend qilish uchun, biz template'ni to'liq yozishimiz kerak yoki original template'ni to'g'ridan-to'g'ri extend qilish kerak.

Lekin SQLAdmin'ning template loader'i avval `templates_dir` da qidiradi, keyin default papkada. Shuning uchun bizning template'imiz topiladi va u o'z-o'zini extend qiladi.

**To'g'ri yondashuv:** Template'larni to'liq override qilish, lekin `sqladmin/layout.html` ni extend qilish (chunki layout bizda ham bor, lekin u to'g'ri ishlaydi).
