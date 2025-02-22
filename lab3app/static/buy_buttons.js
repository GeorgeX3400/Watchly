// Funcția care gestionează adăugarea unui produs în coș
const addToCart = (productId, name, price, quantity) => {
    // Preluăm coșul din localStorage sau inițializăm un array gol
    let cart = JSON.parse(localStorage.getItem('cart') || '[]');
    
    // Căutăm produsul în coș
    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({ id: productId, name: name,price: price, quantity: quantity });
    }

    localStorage.setItem('cart', JSON.stringify(cart));

    updateCart();
};

const removeFromCart = (productId) => {
    let cart = JSON.parse(localStorage.getItem('cart') || '[]');

    cart = cart.filter(item => item.id !== productId);

    localStorage.setItem('cart', JSON.stringify(cart));

    // Actualizăm vizualizarea coșului
    updateCart();
};

const updateCart = () => {
    const cartDisplay = document.getElementById('cart');
    cartDisplay.innerHTML = ''; 

    // add close cart button
    


    const cart = JSON.parse(localStorage.getItem('cart') || '[]');

    if (cart.length === 0) {
        cartDisplay.innerHTML = '<p>Cart is empty :(</p>';
        return;
    }
    // cart items
    const itemList = document.createElement('ul');
    cart.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = `${item.name} ➡ `;
        listItem.style.fontFamily = 'Arial';
        
        const addButton = document.createElement('button');
        addButton.textContent = '+';
        addButton.onclick = () => addToCart(item.id, item.name, item.price, 1);

        const subtractButton = document.createElement('button');
        subtractButton.textContent = '-';
        subtractButton.onclick = () => {
            if (item.quantity > 1) {
                addToCart(item.id, item.name, item.price,  -1);
            } else {
                removeFromCart(item.id);
            }
        };
        const quantityText = document.createElement('a');
        quantityText.textContent = ` ${item.quantity} `;
        quantityText.style.fontWeight = 500;
        
        listItem.appendChild(addButton);
        listItem.appendChild(quantityText);
        listItem.appendChild(subtractButton);
        itemList.appendChild(listItem);
    });

    cartDisplay.appendChild(itemList);
    cartDisplay.insertAdjacentHTML('beforeend', '<a href="../cart">Go to Cart</a>');
};


window.onload = () => {
    console.log("adding listeners.");
    const filtersButton = document.getElementById("filter-button");
    console.log(filtersButton);
    if(filtersButton){
        filtersButton.addEventListener('click', () => {
            const filters = document.getElementsByClassName("filters")[0];
            console.log(filters);
            if(filters.classList.contains("expanded")){
                filters.classList.remove("expanded");
            }
            else {
                filters.classList.add("expanded");
            }
        });
    }
    
    

    const addCartButtons = document.getElementsByClassName('add_to_cart');
    for (let btn of addCartButtons) {
        btn.onclick = () => {
            const productId = btn.dataset.id; // ID-ul produsului
            const quantity = 1; // Cantitatea implicită
            const name = btn.dataset.name;
            const price = btn.dataset.price;
            addToCart(productId, name, price, quantity);
        };
    }

    
    updateCart();
    //cart open/close:
    const cartButton = document.getElementById('cart-button');
    cartButton.addEventListener('click', () => {
        cart = document.getElementById('cart');
        if(cart.style.display == 'block') {
            cart.style.display = 'none';
        }
        else {
            cart.style.display = 'block';
        }
    });

};
