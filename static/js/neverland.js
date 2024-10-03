document.addEventListener('DOMContentLoaded', () => {
    const ingresoField = document.getElementById('ingresoField');
    const ingresarBoton = document.getElementById('ingresarBoton');

    const precioVoucherJuegos = 50; // Asumimos un precio por voucher de juego (puedes cambiarlo según sea necesario)

    ingresarBoton.addEventListener('click', () => {
        const cantidadVouchers = parseInt(ingresoField.value);
        if (!isNaN(cantidadVouchers) && cantidadVouchers > 0) {
            const recaudo = calcularRecaudoVouchersJuegos(cantidadVouchers, precioVoucherJuegos);
            alert(`Recaudo de vouchers de juegos: ${recaudo}`);
        } else {
            alert('Por favor, ingrese una cantidad válida de vouchers.');
        }
    });

    function calcularRecaudoVouchersJuegos(cantidad, precioVoucherJuegos) {
        const recaudoVouchers = precioVoucherJuegos * cantidad;
        setRecaudoJuegos(recaudoVouchers);
        return recaudoVouchers;
    }

    function setRecaudoJuegos(recaudo) {
        // Aquí puedes añadir la lógica para actualizar el recaudo en tu aplicación
        console.log(`Recaudo actualizado: ${recaudo}`);
    }
});
