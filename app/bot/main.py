import asyncio
import json
import logging
from decimal import Decimal
from datetime import datetime
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message, WebAppData, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.enums import ParseMode
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.messages import messages
from app.db import init_db, close_db, get_db, AsyncSessionLocal
from app.models.product import (
    Category, Product, Order, PriceType, OrderStatus
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher with FSM storage
storage = MemoryStorage()
bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)


# FSM States
class PriceCalculationStates(StatesGroup):
    waiting_for_quantity = State()
    waiting_for_area = State()


class OrderStates(StatesGroup):
    waiting_for_quantity = State()
    waiting_for_area = State()


class SearchStates(StatesGroup):
    waiting_for_query = State()


# Helper functions
def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Create main menu keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=messages.BTN_CATALOG)],
            [KeyboardButton(text=messages.BTN_SEARCH)],
            [KeyboardButton(text=messages.BTN_MY_ORDERS)],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


async def get_categories_keyboard() -> InlineKeyboardMarkup:
    """Create categories inline keyboard."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()
    
    if not categories:
        return None
    
    buttons = []
    for category in categories:
        buttons.append([
            InlineKeyboardButton(
                text=category.name,
                callback_data=f"category_{category.id}"
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(
            text=messages.BTN_MAIN_MENU,
            callback_data="main_menu"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_products_keyboard(category_id: int) -> InlineKeyboardMarkup:
    """Create products inline keyboard for a category."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.category_id == category_id)
        )
        products = result.scalars().all()
    
    if not products:
        return None
    
    buttons = []
    for product in products:
        buttons.append([
            InlineKeyboardButton(
                text=product.name,
                callback_data=f"product_{product.id}"
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(
            text=messages.BTN_BACK,
            callback_data="back_to_categories"
        ),
        InlineKeyboardButton(
            text=messages.BTN_MAIN_MENU,
            callback_data="main_menu"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_product_actions_keyboard(product_id: int) -> InlineKeyboardMarkup:
    """Create action buttons for a product."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=messages.BTN_CALCULATE_PRICE,
                    callback_data=f"calc_price_{product_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=messages.BTN_ORDER,
                    callback_data=f"order_{product_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=messages.BTN_BACK,
                    callback_data="back_to_categories"
                ),
                InlineKeyboardButton(
                    text=messages.BTN_MAIN_MENU,
                    callback_data="main_menu"
                )
            ]
        ]
    )
    return keyboard


# Command handlers
@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command."""
    await message.answer(
        f"{messages.WELCOME_MSG}\n\n{messages.MAIN_MENU}",
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    help_text = (
        f"{messages.HELP_MSG}\n\n"
        f"**Mavjud komandalar:**\n"
        f"• /start - Asosiy menyu\n"
        f"• /help - Yordam\n"
        f"• /search - Mahsulot qidirish\n\n"
        f"**Menyu tugmalari:**\n"
        f"• {messages.BTN_CATALOG} - Mahsulotlar katalogi\n"
        f"• {messages.BTN_SEARCH} - Mahsulot qidirish\n"
        f"• {messages.BTN_MY_ORDERS} - Mening buyurtmalarim"
    )
    await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)


@dp.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext):
    """Handle /search command."""
    await message.answer(
        messages.SEARCH_PROMPT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=messages.BTN_MAIN_MENU)]],
            resize_keyboard=True
        )
    )
    await state.set_state(SearchStates.waiting_for_query)


# Message handlers for keyboard buttons
@dp.message(F.text == messages.BTN_CATALOG)
async def handle_catalog(message: Message):
    """Handle catalog button."""
    keyboard = await get_categories_keyboard()
    if keyboard:
        await message.answer(
            f"{messages.CATALOG_TITLE}\n\n{messages.SELECT_CATEGORY}",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.answer(messages.NO_CATEGORIES)


@dp.message(F.text == messages.BTN_SEARCH)
async def handle_search_button(message: Message, state: FSMContext):
    """Handle search button."""
    await message.answer(messages.SEARCH_PROMPT)
    await state.set_state(SearchStates.waiting_for_query)


@dp.message(F.text == messages.BTN_MY_ORDERS)
async def handle_my_orders(message: Message):
    """Handle my orders button."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Order, Product)
            .join(Product, Order.product_id == Product.id)
            .where(Order.user_id == message.from_user.id)
            .order_by(Order.created_at.desc())
        )
        orders_data = result.all()
    
    if not orders_data:
        await message.answer(messages.NO_ORDERS)
        return
    
    response = messages.ORDER_LIST_TITLE
    status_labels = {
        OrderStatus.PENDING: "Qabul qilindi",
        OrderStatus.PROCESSING: "Ko'rib chiqilmoqda",
        OrderStatus.COMPLETED: "Bajarildi",
        OrderStatus.CANCELLED: "Bekor qilindi"
    }
    
    for order, product in orders_data:
        response += messages.ORDER_ITEM.format(
            order_id=order.id,
            product_name=product.name,
            total_price=order.total_price,
            status=status_labels.get(order.status, order.status.value),
            created_at=order.created_at.strftime("%d.%m.%Y %H:%M")
        )
    
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)


@dp.message(F.text == messages.BTN_MAIN_MENU)
async def handle_main_menu(message: Message, state: FSMContext):
    """Handle main menu button."""
    await state.clear()
    await message.answer(
        messages.MAIN_MENU,
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


# Search handler
@dp.message(StateFilter(SearchStates.waiting_for_query))
async def handle_search_query(message: Message, state: FSMContext):
    """Handle search query."""
    if message.text == messages.BTN_MAIN_MENU:
        await handle_main_menu(message, state)
        return
    
    query = message.text.strip()
    if not query:
        await message.answer(messages.SEARCH_PROMPT)
        return
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%")
                )
            ).limit(10)
        )
        products = result.scalars().all()
    
    if not products:
        await message.answer(messages.NO_SEARCH_RESULTS)
        return
    
    response = messages.SEARCH_RESULTS
    buttons = []
    for product in products:
        response += f"• **{product.name}** - {product.price:,.0f} so'm\n"
        buttons.append([
            InlineKeyboardButton(
                text=product.name,
                callback_data=f"product_{product.id}"
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(
            text=messages.BTN_MAIN_MENU,
            callback_data="main_menu"
        )
    ])
    
    await message.answer(
        response,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode=ParseMode.MARKDOWN
    )
    await state.clear()


# Callback query handlers
@dp.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery, state: FSMContext):
    """Handle main menu callback."""
    await state.clear()
    await callback.message.edit_text(
        messages.MAIN_MENU,
        parse_mode=ParseMode.MARKDOWN
    )
    await callback.message.answer(
        messages.MAIN_MENU,
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )
    await callback.answer()


@dp.callback_query(F.data == "back_to_categories")
async def callback_back_to_categories(callback: CallbackQuery):
    """Handle back to categories callback."""
    keyboard = await get_categories_keyboard()
    if keyboard:
        await callback.message.edit_text(
            f"{messages.CATALOG_TITLE}\n\n{messages.SELECT_CATEGORY}",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await callback.message.edit_text(messages.NO_CATEGORIES)
    await callback.answer()


@dp.callback_query(F.data.startswith("category_"))
async def callback_category(callback: CallbackQuery):
    """Handle category selection."""
    category_id = int(callback.data.split("_")[1])
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Category).where(Category.id == category_id)
        )
        category = result.scalar_one_or_none()
        
        if not category:
            await callback.answer(messages.CATEGORY_NOT_FOUND)
            return
        
        result = await session.execute(
            select(Product).where(Product.category_id == category_id)
        )
        products = result.scalars().all()
    
    if not products:
        await callback.message.edit_text(
            messages.NO_PRODUCTS,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text=messages.BTN_BACK,
                        callback_data="back_to_categories"
                    ),
                    InlineKeyboardButton(
                        text=messages.BTN_MAIN_MENU,
                        callback_data="main_menu"
                    )
                ]]
            )
        )
        await callback.answer()
        return
    
    keyboard = await get_products_keyboard(category_id)
    response = messages.PRODUCTS_IN_CATEGORY.format(category_name=category.name)
    
    await callback.message.edit_text(
        response,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("product_"))
async def callback_product(callback: CallbackQuery):
    """Handle product selection."""
    product_id = int(callback.data.split("_")[1])
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product, Category)
            .join(Category, Product.category_id == Category.id)
            .where(Product.id == product_id)
        )
        product_data = result.first()
        
        if not product_data:
            await callback.answer(messages.PRODUCT_NOT_FOUND)
            return
        
        product, category = product_data
    
    # Format product details
    price_type_label = "Dona" if product.price_type == PriceType.DONA else "Kv. metr"
    formatted_price = f"{product.price:,.0f}".replace(",", " ")
    
    description = product.description or "Tavsif mavjud emas."
    
    dimensions = ""
    if product.min_width and product.max_width and product.min_length and product.max_length:
        dimensions = messages.PRODUCT_DIMENSIONS.format(
            min_width=product.min_width,
            max_width=product.max_width,
            min_length=product.min_length,
            max_length=product.max_length
        )
    
    response = messages.PRODUCT_DETAILS.format(
        name=product.name,
        description=description,
        price=formatted_price,
        price_type=price_type_label,
        dimensions=dimensions
    )
    
    keyboard = get_product_actions_keyboard(product_id)
    
    await callback.message.edit_text(
        response,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("calc_price_"))
async def callback_calc_price(callback: CallbackQuery, state: FSMContext):
    """Handle price calculation request."""
    product_id = int(callback.data.split("_")[2])
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        
        if not product:
            await callback.answer(messages.PRODUCT_NOT_FOUND)
            return
    
    await state.update_data(product_id=product_id, product_price_type=product.price_type.value)
    
    if product.price_type == PriceType.DONA:
        await callback.message.answer(messages.ENTER_QUANTITY)
        await state.set_state(PriceCalculationStates.waiting_for_quantity)
    else:
        await callback.message.answer(messages.ENTER_AREA)
        await state.set_state(PriceCalculationStates.waiting_for_area)
    
    await callback.answer()


@dp.message(StateFilter(PriceCalculationStates.waiting_for_quantity))
async def handle_quantity_input(message: Message, state: FSMContext):
    """Handle quantity input for price calculation."""
    if message.text == messages.BTN_MAIN_MENU:
        await handle_main_menu(message, state)
        return
    
    try:
        quantity = float(message.text.replace(",", "."))
        if quantity <= 0:
            raise ValueError()
    except ValueError:
        await message.answer(messages.INVALID_NUMBER)
        return
    
    data = await state.get_data()
    product_id = data.get("product_id")
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        
        if not product:
            await message.answer(messages.PRODUCT_NOT_FOUND)
            await state.clear()
            return
        
        calculated_price = product.calculate_price(quantity=quantity)
    
    response = messages.CALCULATED_PRICE.format(
        price=calculated_price,
        product_name=product.name
    )
    
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)
    await state.clear()


@dp.message(StateFilter(PriceCalculationStates.waiting_for_area))
async def handle_area_input(message: Message, state: FSMContext):
    """Handle area input for price calculation."""
    if message.text == messages.BTN_MAIN_MENU:
        await handle_main_menu(message, state)
        return
    
    try:
        area = float(message.text.replace(",", "."))
        if area <= 0:
            raise ValueError()
    except ValueError:
        await message.answer(messages.INVALID_NUMBER)
        return
    
    data = await state.get_data()
    product_id = data.get("product_id")
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        
        if not product:
            await message.answer(messages.PRODUCT_NOT_FOUND)
            await state.clear()
            return
        
        calculated_price = product.calculate_price(area=area)
    
    response = messages.CALCULATED_PRICE.format(
        price=calculated_price,
        product_name=product.name
    )
    
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)
    await state.clear()


@dp.callback_query(F.data.startswith("order_"))
async def callback_order(callback: CallbackQuery, state: FSMContext):
    """Handle order request."""
    product_id = int(callback.data.split("_")[1])
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        
        if not product:
            await callback.answer(messages.PRODUCT_NOT_FOUND)
            return
    
    await state.update_data(order_product_id=product_id, order_price_type=product.price_type.value)
    
    if product.price_type == PriceType.DONA:
        await callback.message.answer(messages.ENTER_QUANTITY)
        await state.set_state(OrderStates.waiting_for_quantity)
    else:
        await callback.message.answer(messages.ENTER_AREA)
        await state.set_state(OrderStates.waiting_for_area)
    
    await callback.answer()


@dp.message(StateFilter(OrderStates.waiting_for_quantity))
async def handle_order_quantity(message: Message, state: FSMContext):
    """Handle quantity input for order."""
    if message.text == messages.BTN_MAIN_MENU:
        await handle_main_menu(message, state)
        return
    
    try:
        quantity = float(message.text.replace(",", "."))
        if quantity <= 0:
            raise ValueError()
    except ValueError:
        await message.answer(messages.INVALID_NUMBER)
        return
    
    data = await state.get_data()
    product_id = data.get("order_product_id")
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        
        if not product:
            await message.answer(messages.PRODUCT_NOT_FOUND)
            await state.clear()
            return
        
        total_price = product.calculate_price(quantity=quantity)
        
        # Create order
        order = Order(
            user_id=message.from_user.id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            status=OrderStatus.PENDING
        )
        session.add(order)
        await session.commit()
        await session.refresh(order)
    
    status_label = "Qabul qilindi"
    response = messages.ORDER_CONFIRMATION.format(
        product_name=product.name,
        total_price=total_price,
        created_at=order.created_at.strftime("%d.%m.%Y %H:%M"),
        status=status_label
    )
    
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)
    await state.clear()


@dp.message(StateFilter(OrderStates.waiting_for_area))
async def handle_order_area(message: Message, state: FSMContext):
    """Handle area input for order."""
    if message.text == messages.BTN_MAIN_MENU:
        await handle_main_menu(message, state)
        return
    
    try:
        area = float(message.text.replace(",", "."))
        if area <= 0:
            raise ValueError()
    except ValueError:
        await message.answer(messages.INVALID_NUMBER)
        return
    
    data = await state.get_data()
    product_id = data.get("order_product_id")
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        
        if not product:
            await message.answer(messages.PRODUCT_NOT_FOUND)
            await state.clear()
            return
        
        total_price = product.calculate_price(area=area)
        
        # Create order
        order = Order(
            user_id=message.from_user.id,
            product_id=product_id,
            area=area,
            total_price=total_price,
            status=OrderStatus.PENDING
        )
        session.add(order)
        await session.commit()
        await session.refresh(order)
    
    status_label = "Qabul qilindi"
    response = messages.ORDER_CONFIRMATION.format(
        product_name=product.name,
        total_price=total_price,
        created_at=order.created_at.strftime("%d.%m.%Y %H:%M"),
        status=status_label
    )
    
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)
    await state.clear()


# Web App data handler (keep existing)
@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    """Handle data from Telegram Web App (Mini App)."""
    try:
        webapp_data: WebAppData = message.web_app_data
        data = json.loads(webapp_data.data)
        
        logger.info(f"Received web app data: {data}")
        
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
    """Format web app data into a readable Uzbek message."""
    lines = []
    
    if "product_name" in data:
        lines.append(f"📦 **Mahsulot:** {data['product_name']}")
    
    if "product_id" in data:
        lines.append(f"🆔 **ID:** {data['product_id']}")
    
    if "quantity" in data and data["quantity"]:
        lines.append(f"🔢 **Soni:** {data['quantity']}")
    
    if "area" in data and data["area"]:
        lines.append(f"📐 **Maydon:** {data['area']} m²")
    
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


# Unknown message handler
@dp.message()
async def handle_unknown(message: Message):
    """Handle unknown messages."""
    await message.answer(
        messages.UNKNOWN_COMMAND,
        reply_markup=get_main_keyboard()
    )


async def main():
    """Main function to run the bot."""
    try:
        # Import Order model to ensure it's included in Base.metadata
        from app.models.product import Order
        
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
