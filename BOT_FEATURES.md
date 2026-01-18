# Telegram Bot Funksiyalari

Bu hujjatda MarmarX Telegram botining barcha funksiyalari batafsil tavsiflanadi.

## Asosiy Funksiyalar

### 1. Asosiy Menyu

Botni `/start` buyrug'i bilan ishga tushirganda asosiy menyu ko'rsatiladi:

- **📦 Katalog** - Mahsulotlar katalogini ko'rish
- **🔍 Qidirish** - Mahsulotlarni qidirish
- **📋 Mening buyurtmalarim** - Buyurtmalar ro'yxatini ko'rish

### 2. Mahsulotlar Katalogi

**Funksiyalar:**
- Kategoriyalar ro'yxatini ko'rsatish (inline keyboard)
- Kategoriya tanlab mahsulotlarni ko'rish
- Mahsulot tafsilotlarini ko'rish:
  - Nom
  - Tavsif
  - Narx (dona yoki kv.metr)
  - O'lchamlar (agar mavjud bo'lsa)

**Ishlatish:**
1. Asosiy menyudan "📦 Katalog" tugmasini bosing
2. Kategoriyani tanlang
3. Mahsulotni tanlang
4. Mahsulot tafsilotlarini ko'ring

### 3. Narx Hisoblash

**Funksiyalar:**
- Mahsulot tanlangandan keyin narxni hisoblash
- Dona turi uchun: miqdorni kiritish
- Kv.metr turi uchun: maydonni kiritish
- Hisoblangan narxni ko'rsatish

**Ishlatish:**
1. Mahsulotni tanlang
2. "💰 Narxni hisoblash" tugmasini bosing
3. Mahsulot turiga qarab:
   - **Dona**: Miqdorni kiriting (masalan: `5`)
   - **Kv.metr**: Maydonni kiriting (masalan: `10.5`)
4. Hisoblangan narx ko'rsatiladi

### 4. Buyurtma Berish

**Funksiyalar:**
- Mahsulot tanlab buyurtma yaratish
- Buyurtma ma'lumotlarini saqlash
- Buyurtma holatini ko'rish

**Ishlatish:**
1. Mahsulotni tanlang
2. "🛒 Buyurtma berish" tugmasini bosing
3. Miqdor yoki maydonni kiriting
4. Buyurtma yaratiladi va tasdiqlanadi

### 5. Qidiruv

**Funksiyalar:**
- Mahsulotlarni nom bo'yicha qidirish
- Qidiruv natijalarini ko'rsatish
- Tanlangan mahsulotni ko'rish

**Ishlatish:**
1. Asosiy menyudan "🔍 Qidirish" tugmasini bosing
2. Yoki `/search` buyrug'ini kiriting
3. Qidirish so'rovini kiriting (masalan: `marmar`)
4. Natijalarni ko'ring va mahsulotni tanlang

### 6. Mening Buyurtmalarim

**Funksiyalar:**
- Foydalanuvchining barcha buyurtmalarini ko'rish
- Buyurtma holatini ko'rish (Qabul qilindi, Ko'rib chiqilmoqda, Bajarildi)

**Ishlatish:**
1. Asosiy menyudan "📋 Mening buyurtmalarim" tugmasini bosing
2. Barcha buyurtmalar ro'yxati ko'rsatiladi

## Buyruqlar

### `/start`
Botni ishga tushirish va asosiy menyuni ko'rsatish

### `/help`
Yordam xabari va mavjud komandalar ro'yxatini ko'rsatish

### `/search`
Mahsulot qidirish rejimini yoqish

## Keyboard Navigatsiyasi

### Reply Keyboard (Asosiy Menyu)
- Foydalanuvchi qulayligi uchun pastki klaviatura tugmalari
- Har doim ekronda ko'rinib turadi

### Inline Keyboard
- Kategoriyalar va mahsulotlar ro'yxati
- Har bir mahsulot uchun amallar (Narx hisoblash, Buyurtma)
- Navigatsiya tugmalari (Orqaga, Asosiy menyu)

## Mahsulot Turlari

### Dona Turi
- Mahsulot donada sotiladi
- Narx hisoblash uchun miqdor (soni) kerak
- Misol: Vaza, Tayyor mahsulotlar

### Kv.metr Turi
- Mahsulot kv.metrda sotiladi
- Narx hisoblash uchun maydon (kv.metr) kerak
- Misol: Slab, Plita

## Buyurtma Holatlari

1. **Qabul qilindi** (Pending) - Buyurtma yaratildi
2. **Ko'rib chiqilmoqda** (Processing) - Buyurtma ko'rib chiqilmoqda
3. **Bajarildi** (Completed) - Buyurtma bajarildi
4. **Bekor qilindi** (Cancelled) - Buyurtma bekor qilindi

## Xatoliklar

Bot quyidagi xatolarni tushuntirib beradi:

- Mahsulot topilmadi
- Kategoriya topilmadi
- Noto'g'ri ma'lumot kiritildi
- Narxni hisoblashda xatolik

## Texnik Detallar

### FSM (Finite State Machine)
- Narx hisoblash uchun holatlar
- Buyurtma yaratish uchun holatlar
- Qidiruv uchun holatlar

### Database
- Mahsulotlar bazadan yuklanadi
- Buyurtmalar bazaga saqlanadi
- Async SQLAlchemy ishlatiladi

### Xabarlar
- Barcha xabarlar Uzbek tilida
- Markdown formatida formatlangan
- Emoji'lar bilan bezatilgan

## Keyingi Funksiyalar (Kelajakda)

- Sevimli mahsulotlarni saqlash
- Yangi mahsulotlar haqida xabarnomalar
- Buyurtma holatini kuzatish
- Admin funksiyalari botda
- Til tanlash imkoniyati
