import os
import sys
import django
from dbfread import DBF
from django.db import connection

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vales.settings')
django.setup()

from apps.maestros.models.base_models import Servicio

def cargar_servicio_desde_dbf(archivo_dbf):
    """Carga los datos de servicio desde un archivo DBF y los migra al modelo Servicio."""
    
    # Abrir la tabla DBF y leer su contenido
    dbf_table = DBF(archivo_dbf, load=True)

    # Resetear la tabla Servicios (eliminar los datos existentes)
    reset_servicio()

    # Iterar sobre cada registro de la tabla DBF
    for record in dbf_table:
        # Crear el registro en la base de datos
        Servicio.objects.create(
            estatus_servicio=True,  # Asignar True por defecto
            #id_servicio=record['CODIGO'].strip(),
            descripcion_servicio=record['NOMBRE'].strip(),
            importe_servicio=record['IMPORTE'] if record['IMPORTE'] is not None else 0,
            gasto_fijo_servicio=record['GASTOS'] if record['GASTOS'] is not None else 0,
            gasto_porcentaje_servicio=record['GASTOSFIN'] if record['GASTOSFIN'] is not None else 0,
            numero_servicio=record['NUMERO'] if record['NUMERO'] is not None else 0,
            cuota_servicio=record['CUOTA'] if record['CUOTA'] is not None else False,
            plan_servicio=record['PLAN'] if record['PLAN'] is not None else 0,
            posterga_vencimiento=record['RETRASOVTO'] if record['RETRASOVTO'] is not None else 0,
            compro_servicio=record['COMPRO'].strip()
        )

    print(f"Se han migrado {len(dbf_table)} comprobantes de compra de forma exitosa.")

def reset_servicio():
    """Elimina los datos existentes en la tabla Servicio y resetea su ID."""
    # Eliminar los datos existentes en la tabla
    Servicio.objects.all().delete()

    # Reiniciar el autoincremento en la base de datos
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='servicio';")

    print("Datos de la tabla Servicio eliminados y autoincremento reseteado.")

if __name__ == '__main__':
    # Ruta del archivo DBF
    archivo_dbf = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'servicios.dbf')

    # Ejecutar la migración
    cargar_servicio_desde_dbf(archivo_dbf)
