document.addEventListener('DOMContentLoaded', () => {
    const userButtons = document.querySelectorAll('.user-button');
    const backButton = document.getElementById('volver');

    userButtons.forEach(button => {
        button.addEventListener('click', () => {
            fetch(`/login/${button.id}`)
                .then(response => {
                    if (response.ok) {
                        window.location.href = response.url;
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

    //backButton.addEventListener('click', () => {
    //    fetch('/preMenu')
    //        .then(response => {
    //            if (response.ok) {
    //                window.location.href = '/preMenu';
    //            } else {
    //                alert('Error en la redirección. Intenta nuevamente.');
    //            }
    //        })
    //        .catch(error => {
    //            console.error('Error:', error);
    //            alert('Error en la redirección');
    //        });
    //});

    backButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                window.location.href = '/preMenu';
            } else {
                alert('Error al cerrar sesión');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error en la redirección');
        }
    });
});