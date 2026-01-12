# vales\data_load\socio_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from django.db import transaction
from collections import defaultdict
from datetime import datetime

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vales.settings')
django.setup()

from apps.maestros.models.socio_models import Socio, Sucursal
from apps.maestros.models.base_models import *
from apps.maestros.models.sucursal_models import Localidad, Provincia

# Configurar logging
logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'socio_migra.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_progress(current, total, start_time, last_print_time):
    """Muestra el progreso de la migración"""
    elapsed = time.time() - start_time
    percent = (current / total) * 100
    speed = current / elapsed if elapsed > 0 else 0
    
    # Calcular tiempo estimado restante
    remaining = (total - current) / speed if speed > 0 else 0
    remaining_str = time.strftime("%H:%M:%S", time.gmtime(remaining))
    
    print(
        f"\rProgreso: {current:,}/{total:,} ({percent:.1f}%) | "
        f"Velocidad: {speed:.1f} reg/s | "
        f"Tiempo restante: {remaining_str}",
        end='', flush=True
    )
    return time.time()

def reset_socio():
    """Elimina los datos existentes en la tabla Socio y resetea su ID"""
    print("\nInicializando migración...")
    try:
        with transaction.atomic():
            count = Socio.objects.count()
            if count > 0:
                print(f"Eliminando {count:,} registros existentes...")
                Socio.objects.all().delete()
                logger.info(f"Eliminados {count} registros existentes de Socio")
            
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='socio';")
            print("Base de datos preparada para la migración.")
    except Exception as e:
        logger.error(f"Error en reset_socio: {e}")
        raise

def precargar_relaciones():
    """Precarga todas las relaciones necesarias en diccionarios para optimización"""
    print("\nPrecargando relaciones en memoria...")
    logger.info("Precargando relaciones en memoria...")
    
    relaciones = {
        'tipos_doc': defaultdict(
            lambda: TipoDocumentoIdentidad.objects.get(pk=6),  # Valor por defecto
            {
                "CI": TipoDocumentoIdentidad.objects.get(pk=2),
                "CUIT": TipoDocumentoIdentidad.objects.get(pk=1),
                "DNI": TipoDocumentoIdentidad.objects.get(pk=5),
                "LC": TipoDocumentoIdentidad.objects.get(pk=6),
                "LE": TipoDocumentoIdentidad.objects.get(pk=6),
                "OTR": TipoDocumentoIdentidad.objects.get(pk=6)
            }
        ),
        'sucursales': defaultdict(
            lambda: None,
            {s.pk: s for s in Sucursal.objects.all()}
        ),
        'localidades': defaultdict(
            lambda: None,
            {loc.codigo_postal: loc for loc in Localidad.objects.select_related('id_provincia').all()}
        )
    }
    print("Relaciones precargadas en memoria.")
    logger.info("Relaciones precargadas en memoria")
    return relaciones

def procesar_lote(records, cache, current_count, processed_cuits):
    """Procesa un lote de registros y devuelve instancias válidas de Socio"""
    socios = []
    for record in records:
        try:
            # Convertir CODIGO a entero
            try:
                codigo_origen = int(float(record.get('CODIGO', 0)))
            except (ValueError, TypeError):
                logger.warning(f"Valor inválido en CODIGO: {record.get('CODIGO')}. Registro omitido.")
                continue

            # Obtener instancias desde caché
            tipo_iva = TipoIva.objects.get(pk=1)  # Asumiendo IVA Consumidor Final
            tipo_doc = cache['tipos_doc'][record.get('TIPODOC', '').strip()]
            sucursal = cache['sucursales'].get(int(record.get('SUCURSAL', 0))) if record.get('SUCURSAL') else None
            
            # Localidad y provincia
            codigo_postal = str(record.get('CODPOSTAL', ''))[:5] or None
            localidad = cache['localidades'].get(codigo_postal)
            provincia = localidad.id_provincia if localidad else None

            # Manejar fechas
            fecha_alta = record.get('FECING')
            if not fecha_alta or str(fecha_alta).strip() == "":
                fecha_alta = None

            # Crear instancia de Socio
            socio = Socio(
                id_socio=codigo_origen,
                estatus_socio=False,
                codigo_socio=str(record.get('CODIGO')).strip(),
                nombre_socio=record.get('NOMBRE', '').strip(),
                domicilio_socio=record.get('DOMICI', '').strip(),
                codigo_postal=codigo_postal,
                id_localidad=localidad,
                id_provincia=provincia,
                tipo_persona='F', 
                id_tipo_iva=tipo_iva,
                id_tipo_documento_identidad=tipo_doc,
                numero_documento=int(str(record.get('NRODOC')).strip()) if record.get('NRODOC') and str(record.get('NRODOC')).strip() else None,
                cuit=int(str(record.get('CUIT')).strip()) if record.get('CUIT') and str(record.get('CUIT')).strip() else None,
                telefono_socio=record.get('TELEFO', '').strip() or '',
                telefono2_socio=record.get('FAX', '').strip() or '',
                movil_socio=record.get('CELULAR', '').strip() or '',
                email_socio=record.get('MAIL', '').strip() or '',
                fecha_nacimiento=record.get('FECNAC') or None,
                fecha_alta=fecha_alta,
                sexo=record.get('SEXO', 'M').strip() or 'M',
                id_sucursal=sucursal,
            )
            
            # Verificar si cuit ya fue procesado
            if socio.cuit in processed_cuits:
                logger.warning(f"CUIT duplicado: {socio.cuit}. Registro omitido.")
                continue
            processed_cuits.add(socio.cuit)
            
            socios.append(socio)
            
        except Exception as e:
            logger.error(f"Error procesando registro {record.get('CODIGO')}: {str(e)}")
            continue
            
    return socios

def cargar_datos():
    """Función principal de migración con progreso visual"""
    try:
        start_time = time.time()
        last_print_time = start_time
        logger.info("Iniciando migración de socios...")
        print("\nIniciando migración de socios...")
        
        # 1. Resetear datos existentes
        reset_socio()
        # 2. Precargar relaciones en memoria
        cache = precargar_relaciones()
        processed_cuits = set()
        
        # 3. Configuración de procesamiento por lotes
        batch_size = 1000  # Tamaño del lote para bulk_create
        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'socios.DBF')
        total_registros = 0
        
        # 4. Procesamiento optimizado por lotes
        with transaction.atomic():
            # Leer el archivo DBF completo en memoria
            print("\nCargando archivo DBF en memoria...")
            records = list(DBF(dbf_path, encoding='latin-1'))
            total_registros_dbf = len(records)
            print(f"DBF cargado. Total registros a procesar: {total_registros_dbf:,}")
            logger.info(f"DBF cargado en memoria. Total registros: {total_registros_dbf}")
            
            # Procesar en lotes de batch_size
            for i in range(0, total_registros_dbf, batch_size):
                batch_records = records[i:i + batch_size]
                socios_batch = procesar_lote(batch_records, cache, i, processed_cuits)
                
                if socios_batch:
                    Socio.objects.bulk_create(socios_batch)
                    total_registros += len(socios_batch)
                # Mostrar progreso cada 1,000 registros
                if i > 0 and i % 1000 == 0:
                    last_print_time = print_progress(i, total_registros_dbf, start_time, last_print_time)
                
                # Liberar memoria
                del batch_records
                del socios_batch
            
            # Mostrar progreso final
            print_progress(total_registros_dbf, total_registros_dbf, start_time, last_print_time)
            print()  # Nueva línea después del progreso
        
        # 5. Resultados finales
        elapsed_time = time.time() - start_time
        logger.info(
            f"Migración completada. "
            f"Total registros procesados: {total_registros}/{total_registros_dbf}. "
            f"Tiempo: {elapsed_time:.2f} segundos"
        )
        
        print(f"\n{'='*50}")
        print(f"Migración finalizada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Registros procesados: {total_registros:,}/{total_registros_dbf:,}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")
        print(f"Velocidad: {total_registros/elapsed_time:.1f} registros/segundo")
        print(f"{'='*50}")
        
    except Exception as e:
        logger.error(f"Error crítico en cargar_datos: {str(e)}")
        print(f"\nERROR: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos()