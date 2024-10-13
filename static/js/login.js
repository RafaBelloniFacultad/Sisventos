document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerLink = document.getElementById('registerLink');
    const backButton = document.getElementById('backButton');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/auth/auth_login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ usuario: username, contraseña: password }),
            });

            const data = await response.json();

            if (data.success) {
                alert('Inicio de sesión exitoso');
                // Redirect to admin page
                window.location.href = data.redirect;  // Redirige a la página especificada en la respuesta JSON
            } else {
                alert(data.message || 'Usuario o contraseña incorrectos');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al iniciar sesión');
        }
    });

    registerLink.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = '/register';
    });

    backButton.addEventListener('click', () => {
        window.location.href = '/';
    });
});