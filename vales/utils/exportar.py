import sqlite3
import json

def exportar_sqlite_a_json(db_path, json_path):
    conn = sqlite3.connect(db_path)
    conn.text_factory = lambda b: b.decode(errors='ignore')  # Ignorar errores de decodificación
    cursor = conn.cursor()
    
    # Obtener todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    
    datos = {}
    
    for tabla in tablas:
        nombre_tabla = tabla[0]
        try:
            cursor.execute(f"SELECT * FROM {nombre_tabla}")
            columnas = [description[0] for description in cursor.description]
            filas = cursor.fetchall()
            
            datos[nombre_tabla] = []
            for fila in filas:
                fila_dict = {}
                for i, valor in enumerate(fila):
                    # Manejar diferentes tipos de datos
                    if isinstance(valor, bytes):
                        # Intentar decodificar BLOB
                        try:
                            fila_dict[columnas[i]] = valor.decode('utf-8', errors='ignore')
                        except:
                            fila_dict[columnas[i]] = str(valor)
                    elif valor is None:
                        fila_dict[columnas[i]] = None
                    else:
                        fila_dict[columnas[i]] = valor
                
                datos[nombre_tabla].append(fila_dict)
            
            print(f"✓ Tabla '{nombre_tabla}' exportada: {len(filas)} registros")
            
        except Exception as e:
            print(f"✗ Error en tabla '{nombre_tabla}': {e}")
            datos[nombre_tabla] = []
            continue
    
    # Guardar JSON con manejo de errores
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2, default=str)
    
    conn.close()
    print(f"\n✓ Exportación completada: {json_path}")

# Usar
exportar_sqlite_a_json('vales.db', 'datos_vales.json')