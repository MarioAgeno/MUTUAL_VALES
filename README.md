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

## Cuentas Comercio (Backoffice)

Las cuentas de socios se crean desde la app movil por API.

Las Cuentas Comercio se gestionan desde Django backoffice por usuarios staff/superuser.

### Ruta

- Listado: `/maestros/cuenta_comercio/`
- Acceso rapido: menu `Accesos Rapidos -> Cuentas Comercio`

### Operatoria

1. Ingresar a Cuentas Comercio.
2. Crear una vinculacion nueva entre Usuario y Comercio.
3. En alta se puede:
4. Seleccionar usuario existente no vinculado.
5. Crear usuario nuevo y vincularlo en la misma pantalla.
6. Editar o eliminar vinculaciones existentes segun necesidad operativa.


