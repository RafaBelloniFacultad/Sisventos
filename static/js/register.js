document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const backButton = document.getElementById('backButton');

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nombre = document.getElementById('nombre').value;
        const contraseña = document.getElementById('contraseña').value;
        const confirmarContraseña = document.getElementById('confirmarContraseña').value;
        const rol = document.getElementById('rol').value;

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ nombre, contraseña, confirmarContraseña, rol }),
            });

            const data = await response.json();

            if (data.success) {
                alert('Usuario registrado exitosamente');
                window.location.href = '/login';
            } else {
                alert(data.message || 'Ocurrió un error al registrar el usuario');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al registrar el usuario');
        }
    });

    backButton.addEventListener('click', () => {
        window.location.href = '/';
    });
});