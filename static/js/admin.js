document.addEventListener('DOMContentLoaded', () => {
    const adminForm = document.getElementById('adminForm');

    adminForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Evita el comportamiento por defecto del formulario

        // Obtén los valores de los campos
        const diaEvento = document.getElementById('diaEvento').value;
        const mesEvento = document.getElementById('mesEvento').value;
        const cantCom = document.getElementById('cantCom').value;
        const categoriaCom = document.getElementById('categoriaCom').value;
        const nombreCom = document.getElementById('nombreCom').value;
        const stockCom = document.getElementById('stockCom').value;
        const precioUnitarioCom = document.getElementById('precioUnitarioCom').value;
        const precioJuegos = document.getElementById('precioJuegos').value;
        const precioEntradas = document.getElementById('precioEntradas').value;
        const descuentoEntradas = document.getElementById('descuentoEntradas').value;
        const precioCartones = document.getElementById('precioCartones').value;
        const precioEmpanadas = document.getElementById('precioEmpanadas').value;
        const precioPizzas = document.getElementById('precioPizzas').value;
        const precioLocro = document.getElementById('precioLocro').value;

        // Aquí puedes realizar las validaciones necesarias y procesar los datos
        console.log('Datos del evento:');
        console.log(`Día: ${diaEvento}, Mes: ${mesEvento}, Cantidad de comidas: ${cantCom}`);
        console.log(`Categoría de la comida: ${categoriaCom}, Nombre de la comida: ${nombreCom}`);
        console.log(`Stock de la comida: ${stockCom}, Precio unitario de la comida: ${precioUnitarioCom}`);
        console.log(`Precio de los juegos: ${precioJuegos}, Precio de las entradas: ${precioEntradas}`);
        console.log(`Descuento de las entradas: ${descuentoEntradas}, Precio de los cartones: ${precioCartones}`);
        console.log(`Precio de las empanadas: ${precioEmpanadas}, Precio de las pizzas: ${precioPizzas}`);
        console.log(`Precio del locro: ${precioLocro}`);

        // Puedes redirigir a otra página o realizar cualquier otra acción necesaria
        alert('Datos ingresados correctamente');
    });
});
