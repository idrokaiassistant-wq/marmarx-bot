// Telegram WebApp initialization
let tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// Global state
let allProducts = [];
let categories = [];
let selectedCategoryId = null;
let cart = [];

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    await loadProducts();
    renderCategories();
    renderProducts();
    updateCartUI();
});

// Load products from API
async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        if (!response.ok) throw new Error('Failed to fetch products');
        
        const data = await response.json();
        allProducts = data.products || [];
        
        // Extract unique categories from products
        // Group products by category_id to infer category names from product names
        const categoryMap = new Map();
        
        allProducts.forEach(product => {
            if (product.category_id && !categoryMap.has(product.category_id)) {
                // Try to infer category name from first product in category
                // If backend provides category.name, this should be updated
                const categoryName = `Kategoriya ${product.category_id}`;
                categoryMap.set(product.category_id, {
                    id: product.category_id,
                    name: categoryName
                });
            }
        });
        
        categories = Array.from(categoryMap.values());
        
        // Sort categories by ID
        categories.sort((a, b) => (a.id || 0) - (b.id || 0));
        
        // Always add "All" category at the beginning
        categories.unshift({ id: null, name: 'Barchasi' });
        
    } catch (error) {
        console.error('Error loading products:', error);
        showToast('Mahsulotlarni yuklashda xatolik', 'error');
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

// Render categories as tabs
function renderCategories() {
    const categoriesEl = document.getElementById('categories');
    categoriesEl.innerHTML = '';
    
    categories.forEach(category => {
        const btn = document.createElement('button');
        btn.className = `category-tab px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
            selectedCategoryId === category.id 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        }`;
        btn.textContent = category.name;
        btn.onclick = () => {
            selectedCategoryId = category.id;
            renderCategories();
            renderProducts();
        };
        categoriesEl.appendChild(btn);
    });
}

// Render products grid
function renderProducts() {
    const productsEl = document.getElementById('products');
    const noProductsEl = document.getElementById('no-products');
    productsEl.innerHTML = '';
    
    // Filter products by category
    let filteredProducts = allProducts;
    if (selectedCategoryId !== null) {
        filteredProducts = allProducts.filter(p => p.category_id === selectedCategoryId);
    }
    
    if (filteredProducts.length === 0) {
        productsEl.classList.add('hidden');
        noProductsEl.classList.remove('hidden');
        return;
    }
    
    productsEl.classList.remove('hidden');
    noProductsEl.classList.add('hidden');
    
    filteredProducts.forEach(product => {
        const card = createProductCard(product);
        productsEl.appendChild(card);
    });
}

// Create product card
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'bg-white rounded-lg shadow-md overflow-hidden';
    
    const priceDisplay = product.price_type === 'dona' 
        ? `${formatPrice(product.price)} so'm` 
        : `${formatPrice(product.price)} so'm/kv.m`;
    
    card.innerHTML = `
        <div class="p-4">
            <h3 class="font-semibold text-gray-800 mb-1 line-clamp-2 min-h-[2.5rem]">${escapeHtml(product.name)}</h3>
            ${product.description ? `<p class="text-xs text-gray-500 mb-2 line-clamp-2">${escapeHtml(product.description)}</p>` : ''}
            <p class="text-lg font-bold text-blue-600 mb-3">${priceDisplay}</p>
            <button 
                onclick="handleAddToCart(${product.id})"
                class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors"
            >
                Savatga qo'shish
            </button>
        </div>
    `;
    
    return card;
}

// Handle add to cart based on product type
function handleAddToCart(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;
    
    if (product.price_type === 'dona') {
        // Add directly to cart
        addToCart(product, { type: 'dona', quantity: 1 });
        showToast('Mahsulot savatga qo\'shildi', 'success');
    } else if (product.price_type === 'kv_metr') {
        // Open slab modal
        openSlabModal(product);
    }
}

// Open slab modal
let currentSlabProduct = null;

function openSlabModal(product) {
    currentSlabProduct = product;
    const modal = document.getElementById('slab-modal');
    const nameEl = document.getElementById('slab-product-name');
    const descEl = document.getElementById('slab-product-description');
    const widthEl = document.getElementById('slab-width');
    const lengthEl = document.getElementById('slab-length');
    const widthRangeEl = document.getElementById('slab-width-range');
    const lengthRangeEl = document.getElementById('slab-length-range');
    const priceEl = document.getElementById('slab-calculated-price');
    const calcInfoEl = document.getElementById('slab-calculation-info');
    
    nameEl.textContent = product.name;
    descEl.textContent = product.description || '';
    
    // Set min/max for inputs
    const minWidth = product.dimensions?.min_width || 0;
    const maxWidth = product.dimensions?.max_width || 1000;
    const minLength = product.dimensions?.min_length || 0;
    const maxLength = product.dimensions?.max_length || 100;
    
    widthEl.min = minWidth;
    widthEl.max = maxWidth;
    lengthEl.min = minLength;
    lengthEl.max = maxLength;
    
    widthRangeEl.textContent = `Min: ${minWidth} sm, Max: ${maxWidth} sm`;
    lengthRangeEl.textContent = `Min: ${minLength} m, Max: ${maxLength} m`;
    
    // Reset inputs
    widthEl.value = '';
    lengthEl.value = '';
    priceEl.textContent = '0 so\'m';
    calcInfoEl.textContent = '';
    
    // Add event listeners for live calculation
    widthEl.oninput = calculateSlabPrice;
    lengthEl.oninput = calculateSlabPrice;
    
    modal.classList.remove('hidden');
}

function closeSlabModal() {
    document.getElementById('slab-modal').classList.add('hidden');
    currentSlabProduct = null;
}

// Calculate slab price live
function calculateSlabPrice() {
    if (!currentSlabProduct) return;
    
    const width = parseFloat(document.getElementById('slab-width').value) || 0;
    const length = parseFloat(document.getElementById('slab-length').value) || 0;
    const priceEl = document.getElementById('slab-calculated-price');
    const calcInfoEl = document.getElementById('slab-calculation-info');
    
    if (width > 0 && length > 0) {
        // Formula: (width_cm / 100) * length_m * price_per_m2
        const area = (width / 100) * length; // Convert to square meters
        const totalPrice = area * currentSlabProduct.price;
        
        priceEl.textContent = `${formatPrice(totalPrice)} so'm`;
        calcInfoEl.textContent = `(${width} sm / 100) × ${length} m × ${formatPrice(currentSlabProduct.price)} = ${formatPrice(area.toFixed(2))} kv.m × ${formatPrice(currentSlabProduct.price)}`;
    } else {
        priceEl.textContent = '0 so\'m';
        calcInfoEl.textContent = '';
    }
}

// Add slab to cart
function addSlabToCart() {
    if (!currentSlabProduct) return;
    
    const width = parseFloat(document.getElementById('slab-width').value);
    const length = parseFloat(document.getElementById('slab-length').value);
    
    // Validation
    const minWidth = currentSlabProduct.dimensions?.min_width || 0;
    const maxWidth = currentSlabProduct.dimensions?.max_width || 1000;
    const minLength = currentSlabProduct.dimensions?.min_length || 0;
    const maxLength = currentSlabProduct.dimensions?.max_length || 100;
    
    if (!width || width < minWidth || width > maxWidth) {
        showToast(`Kenglik ${minWidth}-${maxWidth} sm oralig'ida bo'lishi kerak`, 'error');
        return;
    }
    
    if (!length || length < minLength || length > maxLength) {
        showToast(`Uzunlik ${minLength}-${maxLength} m oralig'ida bo'lishi kerak`, 'error');
        return;
    }
    
    // Calculate area and price
    const area = (width / 100) * length;
    const totalPrice = area * currentSlabProduct.price;
    
    // Add to cart
    addToCart(currentSlabProduct, {
        type: 'kv_metr',
        width: width,
        length: length,
        area: area,
        totalPrice: totalPrice
    });
    
    showToast('Plita savatga qo\'shildi', 'success');
    closeSlabModal();
}

// Add item to cart
function addToCart(product, options) {
    const cartItem = {
        id: Date.now(), // Unique ID for cart item
        productId: product.id,
        productName: product.name,
        price: product.price,
        priceType: product.price_type,
        ...options
    };
    
    cart.push(cartItem);
    updateCartUI();
}

// Remove item from cart
function removeFromCart(cartItemId) {
    cart = cart.filter(item => item.id !== cartItemId);
    updateCartUI();
}

// Update cart UI
function updateCartUI() {
    const cartCountEl = document.getElementById('cart-count');
    const count = cart.length;
    
    if (count > 0) {
        cartCountEl.textContent = count;
        cartCountEl.classList.remove('hidden');
    } else {
        cartCountEl.classList.add('hidden');
    }
}

// Open cart modal
document.getElementById('cart-btn').onclick = () => {
    const modal = document.getElementById('cart-modal');
    const itemsEl = document.getElementById('cart-items');
    const emptyEl = document.getElementById('cart-empty');
    const summaryEl = document.getElementById('cart-summary');
    const totalEl = document.getElementById('cart-total');
    const checkoutBtn = document.getElementById('checkout-btn');
    
    itemsEl.innerHTML = '';
    
    if (cart.length === 0) {
        emptyEl.classList.remove('hidden');
        summaryEl.classList.add('hidden');
        checkoutBtn.classList.add('hidden');
    } else {
        emptyEl.classList.add('hidden');
        summaryEl.classList.remove('hidden');
        checkoutBtn.classList.remove('hidden');
        
        let total = 0;
        
        cart.forEach(item => {
            const itemEl = document.createElement('div');
            itemEl.className = 'flex justify-between items-start p-3 bg-gray-50 rounded-lg';
            
            let price = 0;
            let details = '';
            
            if (item.priceType === 'dona') {
                price = item.price * (item.quantity || 1);
                details = `${item.quantity || 1} dona`;
            } else if (item.priceType === 'kv_metr') {
                price = item.totalPrice;
                details = `${item.width} sm × ${item.length} m (${item.area.toFixed(2)} kv.m)`;
            }
            
            total += price;
            
            itemEl.innerHTML = `
                <div class="flex-1">
                    <h4 class="font-medium text-gray-800">${escapeHtml(item.productName)}</h4>
                    <p class="text-sm text-gray-500">${details}</p>
                    <p class="text-sm font-semibold text-blue-600 mt-1">${formatPrice(price)} so'm</p>
                </div>
                <button 
                    onclick="removeFromCart(${item.id})"
                    class="ml-3 text-red-500 hover:text-red-700"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                </button>
            `;
            
            itemsEl.appendChild(itemEl);
        });
        
        totalEl.textContent = `${formatPrice(total)} so'm`;
    }
    
    modal.classList.remove('hidden');
};

function closeCartModal() {
    document.getElementById('cart-modal').classList.add('hidden');
}

// Checkout - send data to bot
function checkout() {
    if (cart.length === 0) return;
    
    // Calculate total
    let total = 0;
    const items = cart.map(item => {
        let itemPrice = 0;
        let itemDetails = {};
        
        if (item.priceType === 'dona') {
            itemPrice = item.price * (item.quantity || 1);
            itemDetails = {
                type: 'dona',
                quantity: item.quantity || 1
            };
        } else if (item.priceType === 'kv_metr') {
            itemPrice = item.totalPrice;
            itemDetails = {
                type: 'kv_metr',
                width: item.width,
                length: item.length,
                area: item.area
            };
        }
        
        total += itemPrice;
        
        return {
            productId: item.productId,
            productName: item.productName,
            price: item.price,
            priceType: item.priceType,
            ...itemDetails,
            itemPrice: itemPrice
        };
    });
    
    const orderData = {
        items: items,
        total: total,
        timestamp: new Date().toISOString()
    };
    
    // Send data to Telegram bot
    tg.sendData(JSON.stringify(orderData));
    
    // Show success message
    showToast('Buyurtma yuborildi!', 'success');
    
    // Clear cart
    cart = [];
    updateCartUI();
    closeCartModal();
    
    // Optionally close web app after a delay
    setTimeout(() => {
        tg.close();
    }, 2000);
}

// Utility functions
function formatPrice(price) {
    return new Intl.NumberFormat('uz-UZ').format(Math.round(price));
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    
    const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500';
    
    toast.className = `${bgColor} text-white px-4 py-3 rounded-lg shadow-lg animate-slide-in`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.add('animate-slide-out');
        setTimeout(() => {
            container.removeChild(toast);
        }, 300);
    }, 3000);
}

// Expose functions to global scope for onclick handlers
window.handleAddToCart = handleAddToCart;
window.openSlabModal = openSlabModal;
window.closeSlabModal = closeSlabModal;
window.addSlabToCart = addSlabToCart;
window.removeFromCart = removeFromCart;
window.closeCartModal = closeCartModal;
window.checkout = checkout;
