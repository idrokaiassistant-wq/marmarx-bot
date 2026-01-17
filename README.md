# MarmarX - Marble Selling System

MarmarX - marmar mahsulotlarini sotish uchun to'liq funksional tizim.

## Texnologiyalar

- **FastAPI** - REST API
- **Aiogram 3** - Telegram bot
- **PostgreSQL** - Ma'lumotlar bazasi
- **SQLAlchemy (Async)** - ORM
- **SQLAdmin** - Admin panel
- **Docker** - Konteynerlashtirish

## Loyiha Strukturasi

```
MarmarX/
├── app/
│   ├── core/
│   │   ├── config.py          # Sozlamalar
│   │   └── messages.py        # Uzbek xabarlar
│   ├── models/
│   │   └── product.py         # Category, Product, Service modellari
│   ├── admin/
│   │   └── views.py           # SQLAdmin ko'rinishlari
│   ├── api/
│   │   └── main.py            # FastAPI ilovasi
│   ├── bot/
│   │   └── main.py            # Aiogram bot
│   └── db.py                  # Ma'lumotlar bazasi sozlamalari
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## O'rnatish va Ishga Tushirish

### 1. Sozlamalar

`.env` faylini yarating va quyidagilarni to'ldiring:

```env
DB_URL=postgresql+asyncpg://marmarx:marmarx_password@localhost:5432/marmarx_db
BOT_TOKEN=your_bot_token_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### 2. Docker orqali ishga tushirish

```bash
# Barcha servislarni ishga tushirish
docker-compose up -d

# Loglarni ko'rish
docker-compose logs -f

# To'xtatish
docker-compose down
```

### 3. Lokal ishga tushirish

```bash
# Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Kutubxonalarni o'rnatish
pip install -r requirements.txt

# PostgreSQL ishga tushirish (docker-compose orqali)
docker-compose up -d db

# API ni ishga tushirish
uvicorn app.api.main:app --reload

# Bot ni ishga tushirish
python -m app.bot.main
```

## API Endpointlar

### `GET /`
Asosiy endpoint

### `GET /health`
Sog'liqni tekshirish

### `POST /calculate-price`
Narxni hisoblash

**So'rov:**
```json
{
  "product_id": 1,
  "quantity": 5,        // dona uchun
  "area": 10.5         // kv_metr uchun
}
```

**Javob:**
```json
{
  "product_id": 1,
  "product_name": "Marmar plita",
  "price_type": "kv_metr",
  "calculated_price": 105000.0,
  "message": "Narx hisoblandi: 105,000 so'm"
}
```

### `GET /products`
Barcha mahsulotlarni olish

**Query parametrlar:**
- `category_id` (optional): Kategoriya bo'yicha filtrlash

## Admin Panel

Admin panelga kirish: `http://localhost:8000/admin`

Default foydalanuvchi:
- Username: `admin`
- Password: `admin123`

## Bot Komandalari

- `/start` - Botni ishga tushirish va xush kelibsiz xabari
- `/help` - Yordam xabari

## Web App Data Handler

Bot Web App (Mini App) dan kelgan ma'lumotlarni qabul qiladi va formatlangan Uzbek xabar sifatida ko'rsatadi.

## Modellar

### Category
- `id` - ID
- `name` - Nomi (unique)
- `slug` - Slug (unique)

### Product
- `id` - ID
- `category_id` - Kategoriya ID
- `name` - Nomi
- `description` - Tavsifi
- `price` - Narxi
- `price_type` - Narx turi (`dona` yoki `kv_metr`)
- `min_width`, `max_width` - Min/Max kengligi (sm)
- `min_length`, `max_length` - Min/Max uzunligi (sm)

### Service
- `id` - ID
- `name` - Nomi
- `price` - Narxi
- `context_type` - Kontekst turi (`hovli`, `ofis`, `dom`)

## Til Sozlamalari

Barcha foydalanuvchi xabarlari Uzbek tilida (Lotin yozuvi). Xabarlar `app/core/messages.py` faylida markazlashtirilgan. Keyinchalik boshqa tillarni qo'shish oson.

## Rivojlantirish

### Yangi xabarlar qo'shish

`app/core/messages.py` faylida `Messages` klassiga yangi xabarlar qo'shing:

```python
NEW_MESSAGE = "Yangi xabar"
```

### Ma'lumotlar bazasi migratsiyalari

Alembic ishlatiladi (kelajakda qo'shiladi).

## Muammolarni Hal Qilish

### Bot ishlamayapti
- `.env` faylida `BOT_TOKEN` to'g'ri ekanligini tekshiring
- Bot token @BotFather dan olingan bo'lishi kerak

### Ma'lumotlar bazasi ulanmayapti
- PostgreSQL ishga tushganligini tekshiring
- `DB_URL` to'g'ri ekanligini tekshiring

## Litsenziya

Bu loyiha shaxsiy loyiha.
