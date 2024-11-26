document.addEventListener('DOMContentLoaded', function() {
const eventType = document.getElementById('eventType');
const eventDate = document.getElementById('eventDate');
const foodInputs = document.getElementById('foodInputs');
const foodName = document.getElementById('foodName');
const foodQuantity = document.getElementById('foodQuantity');
const totalCost = document.getElementById('totalCost');
const unitPrice = document.getElementById('unitPrice');
const additionalComments = document.getElementById('additionalComments');
const addFoodButton = document.getElementById('addFoodButton');
const foodList = document.getElementById('foodList');
const submitBuffet = document.getElementById('submitBuffet');
const logoutButton = document.getElementById('logoutButton');

let foods = [];


function updateFormVisibility() {
    if (eventType.value && eventDate.value) {
        foodInputs.style.display = 'block';
        submitBuffet.style.display = 'block';
    } else {
        foodInputs.style.display = 'none';
        submitBuffet.style.display = 'none';
    }
}

eventType.addEventListener('change', updateFormVisibility);
eventDate.addEventListener('input', updateFormVisibility);

addFoodButton.addEventListener('click', function() {
    if (!foodName.value || !foodQuantity.value || !totalCost.value || !unitPrice.value) {
        alert('Por favor, complete todos los campos obligatorios.');
        return;
    }

    const food = {
        name: foodName.value,
        quantity: foodQuantity.value,
        totalCost: totalCost.value,
        unitPrice: unitPrice.value,
        comments: additionalComments.value
    };

    foods.push(food);
    updateFoodList();
    clearFoodInputs();
});

function updateFoodList() {
    foodList.innerHTML = '';
    foods.forEach((food, index) => {
        const foodItem = document.createElement('div');
        foodItem.className = 'food-item';
        foodItem.innerHTML = `
            <div class="food-header" onclick="toggleFoodDetails(${index})">
                <span class="arrow">▶</span>
                <span>${food.name}</span>
            </div>
            <div class="food-details" style="display: none;">
                <p>Cantidad: ${food.quantity}</p>
                <p>Costo Total: ${food.totalCost}</p>
                <p>Precio Unitario: ${food.unitPrice}</p>
                <p>Comentarios: ${food.comments || 'Sin comentarios'}</p>
            </div>
        `;
        foodList.appendChild(foodItem);
    });
}

function clearFoodInputs() {
    foodName.value = '';
    foodQuantity.value = '';
    totalCost.value = '';
    unitPrice.value = '';
    additionalComments.value = '';
}


submitBuffet.addEventListener('click', function() {
    if (foods.length === 0) {
        alert('Por favor, ingrese al menos una comida antes de cargar el buffet.');
        return;
    }

    const eventData = {
        eventType: eventType.value,
        eventDate: eventDate.value,
        foods: foods
    };

    fetch('/submit-buffet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Buffet cargado exitosamente');
            location.reload();
        } else {
            alert('Error al cargar el buffet: ' + (data.message || 'No se proporcionó un mensaje de error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al cargar el buffet: ' + error.message);
    });
});


logoutButton.addEventListener('click', function() {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/login';
        } else {
            alert('Error al cerrar sesión');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al cerrar sesión');
    });
});
});

function toggleFoodDetails(index) {
const foodItem = document.querySelectorAll('.food-item')[index];
const details = foodItem.querySelector('.food-details');
const arrow = foodItem.querySelector('.arrow');
if (details.style.display === 'none') {
    details.style.display = 'block';
    arrow.textContent = '▼';
} else {
    details.style.display = 'none';
    arrow.textContent = '▶';
}
}