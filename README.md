# MUTUAL_VALES
Sistema WEB para gestión y consumo de órdenes de compra en comercios
Desarrollada para la Mutual SEOM de Rafaela
se integra a una APP para ser utilizada por los socios y comercios

## Re-vinculación de dispositivo (Backoffice)

La solicitud de re-vinculación se crea desde la app móvil/dispositivo cuando un socio intenta ingresar desde un equipo distinto al registrado.

En Django backoffice solo se gestionan esas solicitudes ya creadas.

### Pantalla de gestión

- Ruta web: `/usuarios/revinculacion/listar/`
- Acceso: usuarios `staff` del backoffice.
- Búsqueda simple por texto: usuario, device id, plataforma, estado e IP.
- Filtro de estado: Pendiente, Aprobada, Rechazada.

### Acciones disponibles

- Aprobar: aplica el nuevo dispositivo al usuario y sincroniza también con socio cuando existe relación.
- Rechazar: marca la solicitud como rechazada.
- Eliminar: borra la solicitud seleccionada.

### Flujo operativo recomendado

1. Abrir la lista de re-vinculación en backoffice.
2. Buscar al socio por usuario o device id.
3. Revisar estado y datos del nuevo dispositivo.
4. Ejecutar Aprobar o Rechazar según corresponda.
5. Usar Eliminar solo para limpiar solicitudes no necesarias o erróneas.


