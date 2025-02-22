
const getCart = () => JSON.parse(localStorage.getItem('cart') || '[]');


function displayCart() {
  const storedCart = localStorage.getItem('cart');
  const cartItems = storedCart ? JSON.parse(storedCart) : [];

  const sortOption = document.getElementById('sort-option').value;
  console.log(cartItems);
  if (sortOption === 'name') {
    cartItems.sort((a, b) => {
      const nameA = a.name.toLowerCase(); 
      const nameB = b.name.toLowerCase();
      if (nameA < nameB) return -1; 
      if (nameA > nameB) return 1; 
      return 0; 
    });
  } else if (sortOption === 'price') {
    cartItems.sort((a, b) => a.price - b.price);
  }

  const cartContainer = document.getElementById('cart-items');
  cartContainer.innerHTML = '';

  let totalItems = 0;
  let totalPrice = 0;
  let first = cartItems[0];
  console.log(first.id, first.name, first.quantity);
  cartItems.forEach((item) => {
    const listItem = document.createElement('div');
    listItem.className = 'cart-item';
    listItem.innerHTML = `
            <p>${item.name} : 2  x  $${item.price}</p>
            <p>Subtotal: $${(item.price * item.quantity).toFixed(2)}</p>
        `;
    
    totalItems += item.quantity;
    totalPrice += item.price * item.quantity;

    cartContainer.appendChild(listItem);
  });

  document.getElementById('total-items').textContent = `Total Items: ${totalItems}`;
  document.getElementById('total-price').textContent = `Total Price: $${totalPrice.toFixed(2)}`;
}


// find csrf-token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


window.onload = () => {
  displayCart();
  document.getElementById('sort-option').addEventListener('change', (e) => {
    displayCart(e.target.value);
  });

  const buyButton = document.getElementById('buy-button');
  buyButton.addEventListener('click', () => {
    const cart = localStorage.getItem('cart');
    localStorage.setItem(cart, []);
    fetch('http://localhost:8000/order/', {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: cart,
    })
    .then((response) => response.json());
    
  })
};
