document.addEventListener('DOMContentLoaded', () => {
    const adminForm = document.getElementById('adminForm');
    const logoutButton = document.getElementById('logoutButton');

    logoutButton.addEventListener('click', () => {
        fetch('/logout', {
            method: 'POST',  // Asegúrate de que la solicitud sea POST
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/login';  // Redirige después de que la sesión se haya limpiado
            } else {
                alert('Error al cerrar sesión');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al cerrar sesión');
        });
    });
    
    
});

document.addEventListener('DOMContentLoaded', function() {
    const username = 'prueba'; // This should be set dynamically based on the logged-in user
    document.getElementById('username').textContent = username;

    const eventName = document.getElementById('eventName');
    const eventDate = document.getElementById('eventDate');
    const eventDetails = document.getElementById('eventDetails');
    const submitEvent = document.getElementById('submitEvent');
    const bingoSection = document.getElementById('bingoSection');
    const kermesseSection = document.getElementById('kermesseSection');
    const entradasSection = document.getElementById('entradasSection');

    eventName.addEventListener('change', updateFormVisibility);
    eventDate.addEventListener('input', updateFormVisibility);

    function updateFormVisibility() {
        if (eventName.value && isValidDate(eventDate.value)) {
            eventDetails.style.display = 'block';
            submitEvent.style.display = 'block';
            
            if (eventName.value === 'Tombola' || eventName.value === 'Kermesse') {
                bingoSection.style.display = 'block';
                kermesseSection.style.display = 'block';
                entradasSection.style.display = 'block';
            } else {
                bingoSection.style.display = 'none';
                kermesseSection.style.display = 'none';
                entradasSection.style.display = 'none';
            }
        } else {
            eventDetails.style.display = 'none';
            submitEvent.style.display = 'none';
        }
    }

    function isValidDate(dateString) {
        const regex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
        if (!regex.test(dateString)) return false;
        const [, day, month, year] = dateString.match(regex);
        const date = new Date(year, month - 1, day);
        return date.getDate() == day && date.getMonth() == month - 1 && date.getFullYear() == year;
    }

    document.querySelectorAll('.select-button').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            targetElement.style.display = targetElement.style.display === 'none' ? 'block' : 'none';
        });
    });

    document.querySelectorAll('.accept-button').forEach(button => {
        button.addEventListener('click', function() {
            const section = this.closest('.section');
            const inputs = section.querySelectorAll('input');
            let allFilled = true;
            inputs.forEach(input => {
                if (input.hasAttribute('required') && !input.value) {
                    allFilled = false;
                }
            });
            if (allFilled) {
                updateEventRecords(section);
            } else {
                alert('Por favor, complete todos los campos requeridos.');
            }
        });
    });

    submitEvent.addEventListener('click', function() {
        // Here you would typically send the data to the server
        console.log('Submitting event data...');
        // After successful submission, you might want to clear the form
        clearForm();
    });

    document.getElementById('logoutButton').addEventListener('click', function() {
        // Logout logic is already implemented
    });

    function updateEventRecords(section) {
        const eventRecords = document.getElementById('eventRecords');
        const newRecord = document.createElement('div');
        newRecord.className = 'event-record';
        const sectionName = section.querySelector('.select-button').textContent;
        newRecord.innerHTML = `
            <div class="record-header">
                <span class="arrow">▶</span>
                <h3>${sectionName} - ${new Date().toLocaleString()}</h3>
            </div>
            <div class="event-details">
                ${Array.from(section.querySelectorAll('input')).map(input => 
                    `<p>${input.placeholder}: ${input.value}</p>`
                ).join('')}
            </div>
        `;
        newRecord.querySelector('.record-header').addEventListener('click', function() {
            const details = this.nextElementSibling;
            const arrow = this.querySelector('.arrow');
            details.style.display = details.style.display === 'none' ? 'block' : 'none';
            arrow.classList.toggle('open');
        });
        eventRecords.appendChild(newRecord);
    }

    function clearForm() {
        eventName.value = '';
        eventDate.value = '';
        document.querySelectorAll('.details input').forEach(input => input.value = '');
        updateFormVisibility();
    }
});