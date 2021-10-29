const botonEliminar = document.querySelectorAll('.btn-delete')

if (botonEliminar) {
    const listaboton = Array.from(botonEliminar);
    listaboton.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if (!confirm('¿Estas seguro de eliminar esta Cita?')) {
                e.preventDefault();
            }
        })
    })
}