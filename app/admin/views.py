from sqladmin import ModelView
from app.models.product import Category, Product, Service
from app.core.messages import messages


class CategoryAdmin(ModelView, model=Category):
    """Admin view for Category model with Uzbek labels."""
    
    name = "Kategoriya"
    name_plural = "Kategoriyalar"
    icon = "fa-solid fa-folder"
    
    column_list = [Category.id, Category.name, Category.slug]
    column_labels = {
        Category.id: "ID",
        Category.name: "Nomi",
        Category.slug: "Slug"
    }
    
    column_searchable_list = [Category.name, Category.slug]
    column_sortable_list = [Category.id, Category.name]
    
    form_columns = [Category.name, Category.slug]


class ProductAdmin(ModelView, model=Product):
    """Admin view for Product model with Uzbek labels."""
    
    name = "Mahsulot"
    name_plural = "Mahsulotlar"
    icon = "fa-solid fa-cube"
    
    column_list = [
        Product.id,
        Product.category_id,
        Product.name,
        Product.price,
        Product.price_type,
        Product.min_width,
        Product.max_width,
        Product.min_length,
        Product.max_length
    ]
    
    column_labels = {
        Product.id: "ID",
        Product.category_id: "Kategoriya ID",
        Product.name: "Nomi",
        Product.description: "Tavsifi",
        Product.price: "Narxi",
        Product.price_type: "Narx turi",
        Product.min_width: "Min. Kengligi (sm)",
        Product.max_width: "Max. Kengligi (sm)",
        Product.min_length: "Min. Uzunligi (sm)",
        Product.max_length: "Max. Uzunligi (sm)"
    }
    
    column_searchable_list = [Product.name, Product.description]
    column_sortable_list = [Product.id, Product.name, Product.price]
    column_filters = [Product.category_id, Product.price_type]
    
    form_columns = [
        Product.category_id,
        Product.name,
        Product.description,
        Product.price,
        Product.price_type,
        Product.min_width,
        Product.max_width,
        Product.min_length,
        Product.max_length
    ]


class ServiceAdmin(ModelView, model=Service):
    """Admin view for Service model with Uzbek labels."""
    
    name = "Xizmat"
    name_plural = "Xizmatlar"
    icon = "fa-solid fa-tools"
    
    column_list = [Service.id, Service.name, Service.price, Service.context_type]
    
    column_labels = {
        Service.id: "ID",
        Service.name: "Nomi",
        Service.price: "Narxi",
        Service.context_type: "Kontekst turi"
    }
    
    column_searchable_list = [Service.name]
    column_sortable_list = [Service.id, Service.name, Service.price]
    column_filters = [Service.context_type]
    
    form_columns = [Service.name, Service.price, Service.context_type]
