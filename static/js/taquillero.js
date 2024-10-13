document.addEventListener('DOMContentLoaded', () => {
    const ingresoField = document.getElementById('ingresoField');
    const ingresoFieldAnt = document.getElementById('ingresoFieldAnt');
    const ingresarBoton = document.getElementById('ingresarBoton');
    const ingresarBotonAnt = document.getElementById('ingresarBotonAnt');

    ingresarBoton.addEventListener('click', () => {
        const cantidadEntradas = parseInt(ingresoField.value);
        if (!isNaN(cantidadEntradas) && cantidadEntradas > 0) {
            calcularRecaudoEntradas(cantidadEntradas);
        } else {
            alert('Por favor, ingrese una cantidad válida de entradas.');
        }
    });

    ingresarBotonAnt.addEventListener('click', () => {
        const cantidadEntradasAnt = parseInt(ingresoFieldAnt.value);
        if (!isNaN(cantidadEntradasAnt) && cantidadEntradasAnt > 0) {
            calcularRecaudoEntradasAnticipadas(cantidadEntradasAnt);
        } else {
            alert('Por favor, ingrese una cantidad válida de entradas anticipadas.');
        }
    });

    function calcularRecaudoEntradas(cantidad) {
        // Lógica para calcular el recaudo de las entradas vendidas en puerta
        // Ejemplo: const recaudo = precioEntradaPuerta * cantidad;
        alert(`Recaudo de entradas en puerta: ${cantidad}`);
    }

    function calcularRecaudoEntradasAnticipadas(cantidad) {
        // Lógica para calcular el recaudo de las entradas anticipadas
        // Ejemplo: const recaudo = precioEntradaAnticipada * cantidad;
        alert(`Recaudo de entradas anticipadas: ${cantidad}`);
    }
});
