document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-form');
    const passwordField = document.getElementById('password');

    loginForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Evitar el comportamiento por defecto del formulario

        const password = passwordField.value;

        // Aquí deberías verificar la contraseña
        if (password === 'correct_password') { // Reemplaza 'correct_password' con la contraseña correcta
            window.location.href = '/admin';
        } else {
            alert('Contraseña incorrecta');
            passwordField.value = ''; // Limpiar el campo de contraseña
            passwordField.classList.add('error'); // Agregar clase de error
        }
    });

    passwordField.addEventListener('input', () => {
        passwordField.classList.remove('error'); // Remover clase de error al cambiar el texto
    });
});

