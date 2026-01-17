from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

from app.db import get_db, init_db
from app.models.product import Product, PriceType
from app.core.messages import messages
from app.core.config import settings
from sqladmin import Admin
from app.admin.views import CategoryAdmin, ProductAdmin, ServiceAdmin

# Create FastAPI app
app = FastAPI(
    title="MarmarX API",
    description="Marmar sotish tizimi API",
    version="1.0.0"
)

# Session middleware (required for admin authentication)
app.add_middleware(SessionMiddleware, secret_key="marmarx-secret-key-change-in-production")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLAdmin setup
from app.db import engine
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

class AdminAuth(AuthenticationBackend):
    """Simple authentication for admin panel."""
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"authenticated": True})
            return True
        return False
    
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
    
    async def authenticate(self, request: Request) -> bool:
        return request.session.get("authenticated", False)

authentication_backend = AdminAuth(secret_key="marmarx-secret-key-change-in-production")
admin = Admin(
    app, 
    engine, 
    authentication_backend=authentication_backend, 
    title="MarmarX Admin Panel",
    templates_dir="app/templates"
)
admin.add_view(CategoryAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ServiceAdmin)


# Pydantic models for API
class PriceCalculationRequest(BaseModel):
    """Request model for price calculation."""
    product_id: int = Field(..., description="Mahsulot ID")
    quantity: Optional[float] = Field(None, description="Mahsulot soni (dona uchun)")
    area: Optional[float] = Field(None, description="Maydon (kv. metr, kv_metr uchun)")


class PriceCalculationResponse(BaseModel):
    """Response model for price calculation."""
    product_id: int
    product_name: str
    price_type: str
    calculated_price: float
    message: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    message: str


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    from app.db import engine
    await engine.dispose()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "MarmarX API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post(
    "/calculate-price",
    response_model=PriceCalculationResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Mahsulot topilmadi"},
        400: {"model": ErrorResponse, "description": "Noto'g'ri so'rov"}
    }
)
async def calculate_price(
    request: PriceCalculationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Narxni hisoblash endpoint.
    
    Mahsulot turiga qarab:
    - 'dona': quantity (soni) talab qilinadi
    - 'kv_metr': area (maydon) talab qilinadi
    """
    # Get product from database
    result = await db.execute(
        select(Product).where(Product.id == request.product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=404,
            detail=messages.PRODUCT_NOT_FOUND
        )
    
    # Calculate price based on product type
    try:
        if product.price_type == PriceType.DONA:
            if request.quantity is None:
                raise HTTPException(
                    status_code=400,
                    detail="'quantity' (soni) talab qilinadi 'dona' turi uchun"
                )
            calculated_price = product.calculate_price(quantity=request.quantity)
        elif product.price_type == PriceType.KV_METR:
            if request.area is None:
                raise HTTPException(
                    status_code=400,
                    detail="'area' (maydon) talab qilinadi 'kv_metr' turi uchun"
                )
            calculated_price = product.calculate_price(area=request.area)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Noma'lum narx turi: {product.price_type}"
            )
        
        return PriceCalculationResponse(
            product_id=product.id,
            product_name=product.name,
            price_type=product.price_type.value,
            calculated_price=float(calculated_price),
            message=messages.PRICE_CALCULATED.format(price=f"{calculated_price:,.0f}")
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=messages.PRICE_CALCULATION_ERROR
        )


@app.get("/products")
async def get_products(
    category_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Barcha mahsulotlarni olish."""
    query = select(Product)
    if category_id:
        query = query.where(Product.category_id == category_id)
    
    result = await db.execute(query)
    products = result.scalars().all()
    
    return {
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": float(p.price),
                "price_type": p.price_type.value,
                "category_id": p.category_id,
                "dimensions": {
                    "min_width": float(p.min_width) if p.min_width else None,
                    "max_width": float(p.max_width) if p.max_width else None,
                    "min_length": float(p.min_length) if p.min_length else None,
                    "max_length": float(p.max_length) if p.max_length else None,
                }
            }
            for p in products
        ]
    }
