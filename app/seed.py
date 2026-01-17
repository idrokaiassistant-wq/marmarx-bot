"""
Seed script for initial data population.
Boshlang'ich ma'lumotlarni bazaga yozish uchun skript.
"""
import asyncio
from sqlalchemy import select
from app.db import AsyncSessionLocal, engine, Base
from app.models.product import Category, Product, Service, PriceType, ServiceContextType


async def seed_data():
    """Boshlang'ich ma'lumotlarni bazaga yozish."""
    # 1. Jadvallarni yaratish (agar yo'q bo'lsa)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # 2. Baza bo'shligini tekshirish
        result = await session.execute(select(Category))
        if result.scalars().first():
            print("⚠️ Diqqat: Bazada ma'lumotlar allaqachon mavjud.")
            return

        print("⏳ Boshlang'ich ma'lumotlar yozilmoqda...")

        # --- KATEGORIYALAR ---
        cat_slab = Category(name="Maxsus Slablar", slug="slabs")
        cat_zina = Category(name="Zina Elementlari", slug="stairs")
        cat_decor = Category(name="Dekor va Suvenirlar", slug="decor")
        
        session.add_all([cat_slab, cat_zina, cat_decor])
        await session.flush()  # ID larni olish uchun flush qilamiz

        # --- MAHSULOTLAR ---
        
        # 1. Slab (O'lchami o'zgaruvchan - m2 narxda)
        p_slab = Product(
            category_id=cat_slab.id,
            name="Granit Black Galaxy (Slab)",
            description="Qora yaltiroq granit, oshxona va zina uchun.",
            price=450000,  # 1 m2 narxi
            price_type=PriceType.KV_METR,  # Kvadrat metr narxi
            min_width=80,  # sm
            max_width=120,  # sm
            min_length=100,  # sm (1.0 m)
            max_length=300  # sm (3.0 m)
        )

        # 2. Vaza (Dona narxda)
        p_vaza = Product(
            category_id=cat_decor.id,
            name="Marmar Vaza (Oq)",
            description="Qo'lda o'yilgan milliy naqshli vaza.",
            price=150000,  # Dona narxi
            price_type=PriceType.DONA  # Dona mahsulot
        )

        # 3. Zina (Pashod - Dona narxda)
        p_pashod = Product(
            category_id=cat_zina.id,
            name="Granit Pashod (Tayyor)",
            description="Zina uchun tayyor kesilgan tosh.",
            price=120000,
            price_type=PriceType.DONA
        )

        session.add_all([p_slab, p_vaza, p_pashod])

        # --- XIZMATLAR ---
        s_hovli = Service(
            name="Yopishtirish (Hovli)",
            context_type=ServiceContextType.HOVLI,
            price=50000
        )
        s_ofis = Service(
            name="Yopishtirish (Ofis)",
            context_type=ServiceContextType.OFIS,
            price=60000
        )
        s_dom = Service(
            name="Yopishtirish (Kvartira)",
            context_type=ServiceContextType.DOM,
            price=55000
        )
        
        session.add_all([s_hovli, s_ofis, s_dom])

        await session.commit()
        print("✅ Bazaga ma'lumotlar muvaffaqiyatli joylandi!")


if __name__ == "__main__":
    asyncio.run(seed_data())
