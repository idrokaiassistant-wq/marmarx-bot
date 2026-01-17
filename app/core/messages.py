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


# Create a singleton instance
messages = Messages()
