# START HERE - MUTUAL_VALES (Django)

Guia rapida para retomar el backend Django/backoffice.

## 1) Que es este proyecto

Backend principal de administracion y autenticacion JWT (SimpleJWT).
Tambien gestiona backoffice operativo (socios, comercios, aprobaciones, re-vinculacion).

## 2) Rol en arquitectura

- Django (`MUTUAL_VALES`): auth, backoffice, migraciones de schema.
- FastAPI (`MUTUAL_VALES_API`): operaciones moviles.
- Flutter (`mutual_vales_app`): cliente movil.

Importante: Django y FastAPI comparten base de datos. Las migraciones se hacen desde Django.

## 3) Puesta en marcha local

```bash
cd d:\PYTHON\MUTUAL_VALES\vales
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8338
```

## 4) Endpoints moviles clave (Django)

- `POST /usuarios/registro-socio/`
- `POST /usuarios/api/token/`
- `POST /usuarios/api/token/refresh/`
- `GET /usuarios/me/`
- `POST /usuarios/cambiar-contraseña/`
- `POST /usuarios/revincular-dispositivo/`

## 5) Nota funcional importante

En alta de cuenta de socio, se persisten en `usuarios_user`:

- `first_name`
- `last_name`
- `telefono`

Con fallback para `telefono` usando `movil` si aplica.

## 6) Archivos clave

- `vales/apps/usuarios/views/api_views.py`: registro, token, perfil, contraseña.
- `vales/apps/usuarios/serializers.py`: contratos de payload de registro/re-vinculacion.
- `vales/apps/usuarios/models.py`: User custom.
- `README.md`: contexto general.

## 7) Reglas de continuidad

- Cualquier cambio de schema: migrar primero en Django.
- Si cambia JWT/payload auth, validar impacto en FastAPI y Flutter.
- Mantener cambios backward-compatible para endpoints moviles cuando sea posible.
