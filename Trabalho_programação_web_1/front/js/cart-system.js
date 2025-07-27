
class CartManager {
    constructor() {
        this.cart = this.loadCart();
        this.init();
    }

 
    loadCart() {
        const savedCart = localStorage.getItem('gamestore_cart');
        return savedCart ? JSON.parse(savedCart) : [];
    }

    saveCart() {
        localStorage.setItem('gamestore_cart', JSON.stringify(this.cart));
    }

    
    addToCart(product) {
        const existingItem = this.cart.find(item => item.id === product.id);
        
        if (existingItem) {
            existingItem.quantity += product.quantity;
        } else {
            this.cart.push(product);
        }
        
        this.saveCart();
        this.updateCartCount();
        this.showNotification(`${product.name} adicionado ao carrinho!`);
    }

   
    removeFromCart(productId) {
        this.cart = this.cart.filter(item => item.id !== productId);
        this.saveCart();
        this.updateCartCount();
        this.renderCartPage();
    }

    updateQuantity(productId, newQuantity) {
        const item = this.cart.find(item => item.id === productId);
        if (item) {
            if (newQuantity <= 0) {
                this.removeFromCart(productId);
            } else {
                item.quantity = newQuantity;
                this.saveCart();
                this.renderCartPage();
            }
        }
    }

    getCartTotal() {
        return this.cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    getCartItemCount() {
        return this.cart.reduce((count, item) => count + item.quantity, 0);
    }

    updateCartCount() {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = this.getCartItemCount();
        }
    }

   
    showNotification(message) {
     
        const notification = document.createElement('div');
        notification.className = 'cart-notification';
        notification.textContent = message;

        document.body.appendChild(notification);

       
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

 
    renderCartPage() {
        const tbody = document.querySelector('tbody');
        const totalElement = document.querySelector('.cart-total-amount strong');
        
        if (!tbody) return; 

        
        tbody.innerHTML = '';

        if (this.cart.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" class="empty-cart">
                        <p>Seu carrinho está vazio</p>
                        <p>Adicione alguns produtos para continuar</p>
                    </td>
                </tr>
            `;
            if (totalElement) totalElement.textContent = 'R$ 0,00';
            return;
        }

       
        this.cart.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="padding: 15px 0;">
                    <div class="cart-product">
                        <div class="product-icon">
                            ${item.image || '📦'}
                        </div>
                        <div>
                            <div>${item.name}</div>
                            <button onclick="cartManager.removeFromCart('${item.id}')" class="remove-btn">
                                🗑️ Remover
                            </button>
                        </div>
                    </div>
                </td>
                <td style="text-align: center; padding: 15px 0;">R$ ${item.price.toFixed(2).replace('.', ',')}</td>
                <td style="text-align: center; padding: 15px 0;">
                    <div class="quantity-controls">
                        <button onclick="cartManager.updateQuantity('${item.id}', ${item.quantity - 1})" class="quantity-btn">-</button>
                        <input type="number" value="${item.quantity}" min="1" 
                               onchange="cartManager.updateQuantity('${item.id}', parseInt(this.value))"
                               class="quantity-input">
                        <button onclick="cartManager.updateQuantity('${item.id}', ${item.quantity + 1})" class="quantity-btn">+</button>
                    </div>
                </td>
                <td style="text-align: right; padding: 15px 0;">R$ ${(item.price * item.quantity).toFixed(2).replace('.', ',')}</td>
            `;
            tbody.appendChild(row);
        });

       
        if (totalElement) {
            totalElement.textContent = `R$ ${this.getCartTotal().toFixed(2).replace('.', ',')}`;
        }
    }

  
    init() {
        this.updateCartCount();
        
        
        if (window.location.pathname.includes('carrinho.html')) {
            this.renderCartPage();
        }

        
        this.setupProductPageListeners();
    }

    
    setupProductPageListeners() {
        
        const addToCartButtons = document.querySelectorAll('a[href="carrinho.html"].btn');
        
        addToCartButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                
                
                const product = this.extractProductInfo(button);
                if (product) {
                    this.addToCart(product);
                }
            });
        });
    }

   
    extractProductInfo(button) {
        const card = button.closest('.card');
        if (!card) return null;

        let name = 'Produto';
        const sectionTitle = document.querySelector('.section-title');
        const cardTitle = card.querySelector('.card-title');
        
        if (sectionTitle && sectionTitle.textContent.trim() !== 'Placa de video') {
            name = sectionTitle.textContent.trim();
        } else if (cardTitle) {
            name = cardTitle.textContent.trim();
        }

      
        const priceElement = card.querySelector('.card-price');
        let price = 0;
        if (priceElement) {
            const priceText = priceElement.textContent.trim();
          
            const cleanPrice = priceText.replace('R$', '').replace(/\./g, '').replace(',', '.');
            price = parseFloat(cleanPrice) || 0;
        }

    
        const quantityInput = card.querySelector('input[type="number"]');
        const quantity = quantityInput ? parseInt(quantityInput.value) || 1 : 1;

        
        let image = '📦';
        const imageElement = card.querySelector('.card-image img');
        if (imageElement && imageElement.alt) {
            image = imageElement.alt;
        }

        
        const id = name.toLowerCase()
            .replace(/\s+/g, '-')
            .replace(/[^a-z0-9-]/g, '')
            .replace(/-+/g, '-')
            .replace(/^-|-$/g, '');

        return {
            id: id || 'produto-' + Date.now(),
            name,
            price,
            quantity,
            image
        };
    }


    clearCart() {
        this.cart = [];
        this.saveCart();
        this.updateCartCount();
        this.renderCartPage();
        this.showNotification('Carrinho limpo!');
    }
}

let cartManager;
document.addEventListener('DOMContentLoaded', () => {
    cartManager = new CartManager();
});


function clearCart() {
    if (cartManager) {
        cartManager.clearCart();
    }
}

