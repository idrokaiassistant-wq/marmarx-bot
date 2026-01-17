import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, WebAppData
from aiogram.enums import ParseMode

from app.core.config import settings
from app.core.messages import messages
from app.db import init_db, close_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command."""
    await message.answer(
        messages.WELCOME_MSG,
        parse_mode=ParseMode.MARKDOWN
    )


@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    """Handle data from Telegram Web App (Mini App)."""
    try:
        # Parse JSON data from web app
        webapp_data: WebAppData = message.web_app_data
        data = json.loads(webapp_data.data)
        
        logger.info(f"Received web app data: {data}")
        
        # Process the data and format response in Uzbek
        response_text = _format_webapp_response(data)
        
        await message.answer(
            f"{messages.WELCOME_MSG}\n\n"
            f"{messages.WEBAPP_DATA_RECEIVED}\n\n"
            f"{response_text}",
            parse_mode=ParseMode.MARKDOWN
        )
    
    except json.JSONDecodeError:
        logger.error("Failed to parse web app data as JSON")
        await message.answer(
            f"{messages.ERROR_OCCURRED}\n{messages.INVALID_INPUT}"
        )
    except Exception as e:
        logger.error(f"Error processing web app data: {e}", exc_info=True)
        await message.answer(messages.ERROR_OCCURRED)


def _format_webapp_response(data: dict) -> str:
    """
    Format web app data into a readable Uzbek message.
    
    Expected data structure:
    {
        "product_id": int,
        "product_name": str,
        "quantity": float (optional),
        "area": float (optional),
        "price": float,
        "price_type": str,
        ...
    }
    """
    lines = []
    
    # Product information
    if "product_name" in data:
        lines.append(f"📦 **Mahsulot:** {data['product_name']}")
    
    if "product_id" in data:
        lines.append(f"🆔 **ID:** {data['product_id']}")
    
    # Quantity or area
    if "quantity" in data and data["quantity"]:
        lines.append(f"🔢 **Soni:** {data['quantity']}")
    
    if "area" in data and data["area"]:
        lines.append(f"📐 **Maydon:** {data['area']} m²")
    
    # Price information
    if "price" in data:
        price = data["price"]
        if isinstance(price, (int, float)):
            formatted_price = f"{price:,.0f}".replace(",", " ")
            lines.append(f"💰 **Narx:** {formatted_price} so'm")
    
    if "price_type" in data:
        price_type_label = {
            "dona": "Dona",
            "kv_metr": "Kv. metr"
        }.get(data["price_type"], data["price_type"])
        lines.append(f"📊 **Narx turi:** {price_type_label}")
    
    # Additional fields
    if "services" in data and isinstance(data["services"], list):
        if data["services"]:
            lines.append(f"\n🔧 **Xizmatlar:**")
            for service in data["services"]:
                if isinstance(service, dict):
                    service_name = service.get("name", "Noma'lum")
                    service_price = service.get("price", 0)
                    lines.append(f"  • {service_name}: {service_price:,.0f} so'm")
    
    if "total_price" in data:
        total = data["total_price"]
        if isinstance(total, (int, float)):
            formatted_total = f"{total:,.0f}".replace(",", " ")
            lines.append(f"\n💵 **Jami narx:** {formatted_total} so'm")
    
    return "\n".join(lines) if lines else "Ma'lumotlar qayta ishlanmoqda..."


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    await message.answer(messages.HELP_MSG)


@dp.message()
async def handle_unknown(message: Message):
    """Handle unknown commands."""
    await message.answer(messages.UNKNOWN_COMMAND)


async def main():
    """Main function to run the bot."""
    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized")
        
        # Start polling
        logger.info("Starting bot...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
    
    finally:
        await close_db()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
