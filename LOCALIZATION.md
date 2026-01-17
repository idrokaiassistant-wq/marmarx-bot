# SQLAdmin O'zbeklashtirish (Localization)

## Qilingan o'zgarishlar

SQLAdmin interfeysi to'liq o'zbek tiliga o'tkazildi.

### Yaratilgan fayllar

1. **`app/templates/list.html`** - Ro'yxat sahifasi uchun o'zbekcha shablon
   - "Export" → "Yuklab olish"
   - "Search" → "Qidirish"
   - "+ New" → "+ Yangi qo'shish"
   - "Actions" → "Amallar"
   - "No items found" → "Ma'lumot topilmadi"
   - "Delete selected items" → "Tanlanganlarni o'chirish"
   - "Select all" → "Barchasini tanlash"
   - "View" → "Ko'rish"
   - "Edit" → "Tahrirlash"
   - "Delete" → "O'chirish"
   - "prev" → "oldingi"
   - "next" → "keyingi"
   - "Showing X to Y of Z items" → "Ko'rsatilmoqda X dan Y gacha, jami Z ta"
   - "Show X / Page" → "Ko'rsatish X / Sahifa"

2. **`app/templates/layout.html`** - Asosiy layout uchun o'zbekcha shablon
   - "Logout" → "Chiqish"

### Sozlash

`app/api/main.py` faylida `Admin` klassiga `templates_dir="app/templates"` parametri qo'shildi:

```python
admin = Admin(
    app, 
    engine, 
    authentication_backend=authentication_backend, 
    title="MarmarX Admin Panel",
    templates_dir="app/templates"
)
```

### Qo'shimcha tarjimalar

Agar boshqa sahifalar (create, edit, details) uchun ham tarjima kerak bo'lsa, quyidagi fayllarni yaratishingiz mumkin:

- `app/templates/create.html` - Yangi yozuv qo'shish sahifasi
- `app/templates/edit.html` - Tahrirlash sahifasi
- `app/templates/details.html` - Batafsil ko'rish sahifasi
- `app/templates/login.html` - Kirish sahifasi

### Tekshirish

1. Admin panelga kiring: http://localhost:8002/admin
2. Barcha tugmalar va matnlar o'zbek tilida bo'lishi kerak
3. Ro'yxat sahifasida "Yuklab olish", "Qidirish", "Yangi qo'shish", "Amallar" tugmalarini tekshiring
4. Layout'da "Chiqish" tugmasini tekshiring

### Eslatma

SQLAdmin shablonlari Jinja2 sintaksisidan foydalanadi. Shablonlar `sqladmin/` namespace'idan extend qilinadi va kerakli bloklar override qilinadi.
