from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.db import Base


class PriceType(PyEnum):
    """Price type enumeration."""
    DONA = "dona"  # Per piece
    KV_METR = "kv_metr"  # Per square meter


class ServiceContextType(PyEnum):
    """Service context type enumeration."""
    HOVLI = "hovli"  # Yard
    OFIS = "ofis"  # Office
    DOM = "dom"  # House


class Category(Base):
    """Category model for product categorization."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    
    # Relationship
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', slug='{self.slug}')>"


class Product(Base):
    """Product model for marble products.
    
    Supports two pricing types:
    - 'dona' (piece): Fixed price per item (e.g., Vaza)
    - 'kv_metr' (square meter): Price per m² (e.g., Slab)
    """
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(2000), nullable=True)
    price = Column(Numeric(12, 2), nullable=False)
    price_type = Column(SQLEnum(PriceType), nullable=False, default=PriceType.DONA)
    
    # Dimensions (for slabs - min/max width and length)
    min_width = Column(Numeric(10, 2), nullable=True)  # in cm
    max_width = Column(Numeric(10, 2), nullable=True)  # in cm
    min_length = Column(Numeric(10, 2), nullable=True)  # in cm
    max_length = Column(Numeric(10, 2), nullable=True)  # in cm
    
    # Relationship
    category = relationship("Category", back_populates="products")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, price_type='{self.price_type.value}')>"
    
    def calculate_price(self, quantity: float = 1.0, area: float = None) -> float:
        """
        Calculate price based on product type.
        
        Args:
            quantity: Number of pieces (for 'dona' type)
            area: Area in square meters (for 'kv_metr' type)
        
        Returns:
            Calculated price
        """
        if self.price_type == PriceType.DONA:
            return float(self.price) * quantity
        elif self.price_type == PriceType.KV_METR:
            if area is None:
                raise ValueError("Area is required for square meter pricing")
            return float(self.price) * area
        else:
            raise ValueError(f"Unknown price type: {self.price_type}")


class Service(Base):
    """Service model for additional services."""
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    price = Column(Numeric(12, 2), nullable=False)
    context_type = Column(SQLEnum(ServiceContextType), nullable=False)
    
    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}', price={self.price}, context_type='{self.context_type.value}')>"
