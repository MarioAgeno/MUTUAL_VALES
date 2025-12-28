# MUTUAL_VALES
Sistema WEB para consumos de vales de compras en comercios

flowchart TD
    A[Descarga App] --> B[Ingreso CUIT, Tel, Email]
    B --> C[Verificación SMS + Email]
    C --> D[Solicitud pendiente en Backoffice]
    D --> E[Empleado valida datos en base]
    E --> F{Datos correctos?}
    F -->|Sí| G[Aprobación]
    G --> H[Usuario crea password]
    H --> I[Acceso a App]
    F -->|No| J[Rechazo]
    J --> K[Debe asociarse en la mutual]
