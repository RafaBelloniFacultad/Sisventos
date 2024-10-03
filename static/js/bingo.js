document.addEventListener('DOMContentLoaded', () => {
    const tiradaArea = document.getElementById('tiradaArea');
    const actualizarTirada = document.getElementById('actualizarTirada');
    const ingresoField = document.getElementById('ingresoField');
    const ingresarBoton = document.getElementById('ingresarBoton');

    const cantTiradas = 3; // Cantidad máxima de tiradas
    let numTirada = 1;
    const precioCartonBingo = 100; // Asumimos un precio por cartón de bingo (puedes cambiarlo según sea necesario)

    actualizarTirada.addEventListener('click', () => {
        const confirmacion = confirm('¿Seguro que desea actualizar la tirada? Solo hay 3 tiradas disponibles.');
        if (confirmacion) {
            numTirada = actualizarTiradaFunction(numTirada, cantTiradas);
            tiradaArea.value = `Tirada N°: ${numTirada}`;
        }
    });

    ingresarBoton.addEventListener('click', () => {
        const cantidadCartones = parseInt(ingresoField.value);
        if (!isNaN(cantidadCartones) && cantidadCartones > 0) {
            const recaudo = calcularRecaudoCartonesBingo(cantidadCartones, precioCartonBingo);
            alert(`Recaudo de cartones de bingo: ${recaudo}`);
        } else {
            alert('Por favor, ingrese una cantidad válida de cartones.');
        }
    });

    function actualizarTiradaFunction(numTirada, cantTiradas) {
        if (numTirada < cantTiradas) {
            numTirada++;
        }
        return numTirada;
    }

    function calcularRecaudoCartonesBingo(cantidad, precioCartonBingo) {
        const recaudoCartones = precioCartonBingo * cantidad;
        setRecaudoBingo(recaudoCartones);
        return recaudoCartones;
    }

    function setRecaudoBingo(recaudo) {
        // Aquí puedes añadir la lógica para actualizar el recaudo en tu aplicación
        console.log(`Recaudo actualizado: ${recaudo}`);
    }
});

