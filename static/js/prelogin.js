document.addEventListener('DOMContentLoaded', () => {
    const gestionarButton = document.getElementById('gestionar');
    const cargarButton = document.getElementById('cargar');

    gestionarButton.addEventListener('click', () => {
        fetch('/preMenu', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/preMenu';
            } else {
                alert('Error en la redirección. Intenta nuevamente.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error en la redirección');
        });
    });

    cargarButton.addEventListener('click', () => {
        fetch('/login', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/login';
            } else {
                alert('Error en la redirección. Intenta nuevamente.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error en la redirección');
        });
    });
});