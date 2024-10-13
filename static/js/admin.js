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
