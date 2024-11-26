document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const codigoEvento = document.getElementById('codigoEvento');
    const backButton = document.getElementById('backButton');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch('/verificar-evento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    codigo: codigoEvento.value
                })
            });

            const data = await response.json();

            if (data.exists) {
                window.location.href = '/menu';
            } else {
                alert('Error: No se cargó ningún evento con ese código de día');
                codigoEvento.value = ''; // Limpiamos el campo
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al verificar el código de evento');
        }
    });

    backButton.addEventListener('click', () => {
        window.location.href = '/';
    });
});