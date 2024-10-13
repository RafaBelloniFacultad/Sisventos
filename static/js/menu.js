document.addEventListener('DOMContentLoaded', () => {
    let selectedUser = '';

    const userButtons = document.querySelectorAll('.user-button');
    const loginButton = document.getElementById('ingresar');

    userButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation(); // Evita que el evento se propague al documento
            userButtons.forEach(btn => btn.style.backgroundColor = '#336699'); // Reset background color
            button.style.backgroundColor = '#224466'; // Highlight selected button
            selectedUser = button.id;
        });
    });

    loginButton.addEventListener('click', () => {
        if (selectedUser) {
            // En lugar de window.location.href, realizamos una redirección en Flask
            fetch(`/login/${selectedUser}`)
                .then(response => {
                    if (response.ok) {
                        window.location.href = response.url; // Redirige a la URL devuelta por el servidor
                    } else {
                        alert('Error en la redirección. Intenta nuevamente.');
                    }
                })
                .catch(error => {
                    console.error('Hubo un error en la redirección:', error);
                });
        } else {
            alert('Por favor, seleccione un tipo de usuario antes de ingresar.');
        }
    });

    document.addEventListener('click', (event) => {
        if (!event.target.classList.contains('user-button')) {
            userButtons.forEach(btn => btn.style.backgroundColor = '#336699'); // Reset background color
            selectedUser = '';
        }
    });
});
