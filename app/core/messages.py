"""
Messages module for MarmarX.
All user-facing strings are in Uzbek (Latin script).
Future-proofed for easy addition of other languages.
"""


class Messages:
    """Centralized message storage for the application."""
    
    # Welcome messages
    WELCOME_MSG = "Assalomu alaykum! MarmarX botiga xush kelibsiz! 🏛️\n\n" \
                  "Bizning bot orqali marmar mahsulotlarini ko'rib chiqishingiz va " \
                  "narxlarni hisoblashingiz mumkin."
    
    # Order messages
    ORDER_RECEIVED = "Buyurtmangiz qabul qilindi! ✅"
    ORDER_PROCESSING = "Buyurtmangiz ko'rib chiqilmoqda..."
    ORDER_COMPLETED = "Buyurtmangiz bajarildi!"
    
    # Product messages
    PRODUCT_NOT_FOUND = "Mahsulot topilmadi."
    CATEGORY_NOT_FOUND = "Kategoriya topilmadi."
    
    # Price calculation
    PRICE_CALCULATED = "Narx hisoblandi: {price} so'm"
    PRICE_CALCULATION_ERROR = "Narxni hisoblashda xatolik yuz berdi."
    
    # Errors
    ERROR_OCCURRED = "Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
    INVALID_INPUT = "Noto'g'ri ma'lumot kiritildi."
    
    # Admin
    ADMIN_ACCESS_DENIED = "Admin huquqi talab qilinadi."
    
    # Web App Data
    WEBAPP_DATA_RECEIVED = "Ma'lumotlar qabul qilindi!"
    WEBAPP_DATA_PROCESSING = "Ma'lumotlaringiz qayta ishlanmoqda..."
    
    # General
    HELP_MSG = "Yordam olish uchun /start buyrug'ini bosing."
    UNKNOWN_COMMAND = "Noma'lum buyruq. /start buyrug'ini bosing."
    
    # Product details
    PRODUCT_NAME = "Mahsulot nomi"
    PRODUCT_PRICE = "Narxi"
    PRODUCT_DESCRIPTION = "Tavsifi"
    PRODUCT_DIMENSIONS = "O'lchamlari"
    PRODUCT_PRICE_TYPE = "Narx turi"
    
    # Price types
    PRICE_TYPE_PIECE = "dona"
    PRICE_TYPE_SQUARE_METER = "kv_metr"
    
    # Service types
    SERVICE_HOVLI = "hovli"
    SERVICE_OFIS = "ofis"
    SERVICE_DOM = "dom"
    
    # Catalog messages
    CATALOG_TITLE = "📦 Mahsulotlar katalogi"
    SELECT_CATEGORY = "Kategoriyani tanlang:"
    NO_CATEGORIES = "Kategoriyalar topilmadi."
    PRODUCTS_IN_CATEGORY = "📂 {category_name} kategoriyasi:"
    NO_PRODUCTS = "Bu kategoriyada mahsulotlar topilmadi."
    PRODUCT_DETAILS = "📦 **{name}**\n\n" \
                      "{description}\n\n" \
                      "💰 **Narx:** {price} so'm ({price_type})\n" \
                      "{dimensions}"
    PRODUCT_DIMENSIONS = "📐 **O'lchamlar:** {min_width}-{max_width} x {min_length}-{max_length} sm"
    PRODUCT_NO_DIMENSIONS = ""
    
    # Price calculation
    ENTER_QUANTITY = "Miqdorni kiriting (dona):"
    ENTER_AREA = "Maydonni kiriting (kv. metr):"
    CALCULATED_PRICE = "✅ **Hisoblangan narx:** {price:,.0f} so'm\n" \
                       "Mahsulot: {product_name}"
    INVALID_NUMBER = "Noto'g'ri raqam kiritildi. Iltimos, raqam kiriting."
    
    # Order messages
    ORDER_CONFIRMATION = "✅ **Buyurtma yaratildi!**\n\n" \
                         "📦 Mahsulot: {product_name}\n" \
                         "💰 Jami narx: {total_price:,.0f} so'm\n" \
                         "📅 Sana: {created_at}\n" \
                         "📊 Holat: {status}"
    ORDER_LIST_TITLE = "📋 **Sizning buyurtmalaringiz:**\n"
    ORDER_ITEM = "\n📦 **Buyurtma #{order_id}**\n" \
                 "Mahsulot: {product_name}\n" \
                 "Narx: {total_price:,.0f} so'm\n" \
                 "Holat: {status}\n" \
                 "Sana: {created_at}"
    NO_ORDERS = "Sizda hozircha buyurtmalar yo'q."
    
    # Search messages
    SEARCH_PROMPT = "Qidirish uchun mahsulot nomini kiriting:"
    SEARCH_RESULTS = "🔍 **Qidiruv natijalari:**\n\n"
    NO_SEARCH_RESULTS = "Hech qanday mahsulot topilmadi."
    
    # Keyboard labels
    BTN_CATALOG = "📦 Katalog"
    BTN_MY_ORDERS = "📋 Mening buyurtmalarim"
    BTN_SEARCH = "🔍 Qidirish"
    BTN_BACK = "◀️ Orqaga"
    BTN_MAIN_MENU = "🏠 Asosiy menyu"
    BTN_CALCULATE_PRICE = "💰 Narxni hisoblash"
    BTN_ORDER = "🛒 Buyurtma berish"
    
    # Navigation
    MAIN_MENU = "🏠 **Asosiy menyu**\n\n" \
                "Kerakli bo'limni tanlang:"
    GO_BACK = "Orqaga qaytildi."


# Create a singleton instance
messages = Messages()
