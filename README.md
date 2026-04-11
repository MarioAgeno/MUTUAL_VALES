# MUTUAL_VALES (Django)

Sistema web de gestión y backoffice para Órdenes de Compra.

- Gestión operativa y administrativa.
- Autenticación JWT (SimpleJWT) consumida por la app móvil.
- Administración de entidades maestras (socios, comercios, planes, etc.).
- Gestión de seguridad y re-vinculación de dispositivos.

Desarrollada para la Mutual SEOM de Rafaela.

## Rol dentro de la arquitectura

El ecosistema está compuesto por 3 proyectos:

1. Django (`MUTUAL_VALES`): fuente de verdad de autenticación y backoffice.
2. FastAPI (`MUTUAL_VALES_API`): operaciones móviles (adhesión, vales, compras).
3. Flutter (`mutual_vales_app`): cliente móvil para socios y comercios.

Puntos clave:

- Django y FastAPI comparten la misma base de datos.
- Las migraciones de esquema se gestionan desde Django.
- La app Flutter consume endpoints de Django y FastAPI en paralelo.

## Puesta en marcha rápida

```bash
cd vales
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8338
```

## Endpoints API clave de Django para la app móvil

- `POST /usuarios/registro-socio/`
- `POST /usuarios/api/token/`
- `POST /usuarios/api/token/refresh/`
- `GET /usuarios/me/`
- `POST /usuarios/cambiar-contraseña/`
- `POST /usuarios/revincular-dispositivo/`

## Alta de cuenta socio

Cuando un usuario crea su cuenta desde la app, Django persiste en `usuarios_user`:

- `first_name`
- `last_name`
- `telefono`

Además, se vincula usuario-socio y se asigna grupo `Usuario`.

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

## Recomendaciones para continuidad del proyecto

1. Mantener sincronizados contratos de API con la app Flutter.
2. Documentar en el commit cualquier cambio de endpoint, payload o validación.
3. Si se modifica autenticación o claims JWT, validar también impacto en FastAPI.
4. Priorizar cambios backward-compatible en endpoints móviles.


