
function fetchCSRFToken() {
    const response = fetch('http://localhost:8000/get-token/', method='GET')
    .then(response => response.json);
    token = response.token;
    
    document.cookie = `csrf-token=${token};`
}

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