# Define las columnas Bootstrap y sección para cada campo


class Design:
	checkbox = "checkbox"


estructura_campos = {
	
	'actividad': {
		'Información Actividad': {
			'fila_1': [
				{'field_name': 'estatus_actividad', 'columna': 2, 'design': None},
				{'field_name': 'descripcion_actividad', 'columna': 4, 'design': None},
				{'field_name': 'fecha_registro_actividad', 'columna': 2, 'design': None}
			]
		}
	},
	
	
	'provincia': {
		'Información Provincia': {
			'fila_1': [
				{'field_name': 'estatus_provincia', 'columna': 2, 'design': None},
				{'field_name': 'codigo_provincia', 'columna': 1, 'design': None},
				{'field_name': 'nombre_provincia', 'columna': 3, 'design': None},
			]
		}
	},
	
	'localidad': {
		'Información Localidad': {
			'fila_1': [
				{'field_name': 'estatus_localidad', 'columna': 2, 'design': None},
				{'field_name': 'nombre_localidad', 'columna': 3, 'design': None},
				{'field_name': 'codigo_postal', 'columna': 2, 'design': None},
				{'field_name': 'id_provincia', 'columna': 3, 'design': None},
			]
		}
	},
	
	'tipo_documento_identidad': {
		'Información Tipo Documento Identidad': {
			'fila_1': [
				{'field_name': 'estatus_tipo_documento_identidad', 'columna': 2, 'design': None},
				{'field_name': 'nombre_documento_identidad', 'columna': 2, 'design': None},
				{'field_name': 'tipo_documento_identidad', 'columna': 2, 'design': None},
				{'field_name': 'codigo_afip', 'columna': 2, 'design': None},
				{'field_name': 'ws_afip', 'columna': 2, 'design': None},
			]
		}
	},
	
	'tipo_iva': {
		'Información Tipo I.V.A.': {
			'fila_1': [
				{'field_name': 'estatus_tipo_iva', 'columna': 2, 'design': None},
				{'field_name': 'codigo_iva', 'columna': 2, 'design': None},
				{'field_name': 'nombre_iva', 'columna': 3, 'design': None},
				{'field_name': 'discrimina_iva', 'columna': 2, 'design': Design.checkbox},
			]
		}
	},
	
	'cliente': {
		'Información General': {
			'fila_1': [
				{'field_name': 'estatus_cliente', 'columna': 2, 'design': None},
				{'field_name': 'nombre_cliente', 'columna': 4, 'design': None},
				{'field_name': 'domicilio_cliente', 'columna': 6, 'design': None},
			],
			'fila_2': [
				{'field_name': 'codigo_postal', 'columna': 2, 'design': None},
				{'field_name': 'id_provincia', 'columna': 4, 'design': None},
				{'field_name': 'id_localidad', 'columna': 4, 'design': None},
			],
			'fila_3': [
				{'field_name': 'tipo_persona', 'columna': 2, 'design': None},
				{'field_name': 'id_tipo_documento_identidad', 'columna': 2, 'design': None},
				{'field_name': 'cuit', 'columna': 2, 'design': None},
				{'field_name': 'id_tipo_iva', 'columna': 2, 'design': None},
				{'field_name': 'condicion_venta', 'columna': 2, 'design': None},
			],
			'fila_4': [
				{'field_name': 'telefono_cliente', 'columna': 2, 'design': None},
				{'field_name': 'fax_cliente', 'columna': 2, 'design': None},
				{'field_name': 'movil_cliente', 'columna': 2, 'design': None},
				{'field_name': 'email_cliente', 'columna': 3, 'design': None},
				{'field_name': 'email2_cliente', 'columna': 3, 'design': None},
			],
			'fila_5': [
				{'field_name': 'transporte_cliente', 'columna': 3, 'design': None},
				{'field_name': 'id_vendedor', 'columna': 3, 'design': None},
				{'field_name': 'fecha_nacimiento', 'columna': 2, 'design': None},
				{'field_name': 'fecha_alta', 'columna': 2, 'design': None},
				{'field_name': 'sexo', 'columna': 2, 'design': None},
			],
			'fila_6': [
				{'field_name': 'id_actividad', 'columna': 3, 'design': None},
				{'field_name': 'id_sucursal', 'columna': 3, 'design': None},
				{'field_name': 'id_percepcion_ib', 'columna': 3, 'design': None},
				{'field_name': 'numero_ib', 'columna': 3, 'design': None},
			],
			'fila_7': [
				{'field_name': 'vip', 'columna': 2, 'design': None},
				{'field_name': 'mayorista', 'columna': 2, 'design': None},
				{'field_name': 'sub_cuenta', 'columna': 2, 'design': None},
				{'field_name': 'observaciones_cliente', 'columna': 6, 'design': None},
			],
			# Agrega más filas o campos según sea necesario
		},
		'Black List': {
			'fila_1': [
				{'field_name': 'black_list', 'columna': 2, 'design': None},
				{'field_name': 'black_list_motivo', 'columna': 5, 'design': None},
				{'field_name': 'black_list_usuario', 'columna': 3, 'design': None},
				{'field_name': 'fecha_baja', 'columna': 2, 'design': None},
			],
		},
	},
	
	'proveedor': {
		'Información Proveedor': {
			'fila_1': [
				{'field_name': 'estatus_proveedor', 'columna': 2, 'design': None},
				{'field_name': 'nombre_proveedor', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'domicilio_proveedor', 'columna': 4, 'design': None},
				{'field_name': 'id_localidad', 'columna': 2, 'design': None},
				{'field_name': 'codigo_postal', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'telefono_proveedor', 'columna': 2, 'design': None},
				{'field_name': 'movil_proveedor', 'columna': 2, 'design': None},
				{'field_name': 'email_proveedor', 'columna': 4, 'design': None},
			],
			'fila_4': [
				{'field_name': 'ib_numero', 'columna': 2, 'design': None},
				{'field_name': 'cuit', 'columna': 2, 'design': None},
				{'field_name': 'id_tipo_iva', 'columna': 2, 'design': None},
			],
			'fila_5': [
				{'field_name': 'id_tipo_retencion_ib', 'columna': 4, 'design': None},
				{'field_name': 'ib_alicuota', 'columna': 2, 'design': None},
				{'field_name': 'ib_exento', 'columna': 2, 'design': Design.checkbox},
				{'field_name': 'multilateral', 'columna': 3, 'design': Design.checkbox},
			],
			'fila_6': [
				{'field_name': 'observacion_proveedor', 'columna': 10, 'design': None},
			],
		}
	},
	
	'parametro': {
		'Información Parámetros': {
			'fila_1': [
				{'field_name': 'estatus_parametro', 'columna': 2, 'design': None},
				{'field_name': 'id_empresa', 'columna': 8, 'design': None},
			],
			'fila_2': [
				{'field_name': 'interes', 'columna': 2, 'design': None},
				{'field_name': 'interes_dolar', 'columna': 2, 'design': None},
				{'field_name': 'cotizacion_dolar', 'columna': 2, 'design': None},
				{'field_name': 'dias_vencimiento', 'columna': 2, 'design': None},
				{'field_name': 'descuento_maximo', 'columna': 2, 'design': None},
			],
		}
	},
	
	'sucursal': {
		'Información Sucursal': {
			'fila_1': [
				{'field_name': 'estatus_sucursal', 'columna': 2, 'design': None},
				{'field_name': 'nombre_sucursal', 'columna': 4, 'design': None},
				{'field_name': 'codigo_michelin', 'columna': 2, 'design': None},
			],
			'fila_2': [
				{'field_name': 'domicilio_sucursal', 'columna': 4, 'design': None},
				{'field_name': 'id_localidad', 'columna': 2, 'design': None},
				{'field_name': 'id_provincia', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'telefono_sucursal', 'columna': 2, 'design': None},
				{'field_name': 'email_sucursal', 'columna': 4, 'design': None},
				{'field_name': 'inicio_actividad', 'columna': 2, 'design': None},
			],
		}
	},
	
	'empresa': {
		'Información Empresa': {
			'fila_1': [
				{'field_name': 'estatus_empresa', 'columna': 2, 'design': None},
				{'field_name': 'nombre_fiscal', 'columna': 4, 'design': None},
				{'field_name': 'nombre_comercial', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'domicilio_empresa', 'columna': 4, 'design': None},
				{'field_name': 'codigo_postal', 'columna': 2, 'design': None},
				{'field_name': 'id_localidad', 'columna': 3, 'design': None},
				{'field_name': 'id_provincia', 'columna': 3, 'design': None},
			],
			'fila_3': [
				{'field_name': 'telefono', 'columna': 2, 'design': None},
				{'field_name': 'email_empresa', 'columna': 4, 'design': None},
				{'field_name': 'web_empresa', 'columna': 4, 'design': None},
				{'field_name': 'logo_empresa', 'columna': 2, 'design': None},
			],
			'fila_4': [
				{'field_name': 'id_iva', 'columna': 3, 'design': None},
				{'field_name': 'cuit', 'columna': 2, 'design': None},
				{'field_name': 'ingresos_bruto', 'columna': 2, 'design': None},
				{'field_name': 'inicio_actividad', 'columna': 2, 'design': None},
			],
			'fila_5': [
				{'field_name': 'cbu', 'columna': 3, 'design': None},
				{'field_name': 'cbu_alias', 'columna': 4, 'design': None},
				{'field_name': 'cbu_vence', 'columna': 2, 'design': None},
			],
			'fila_6': [
				{'field_name': 'ws_archivo_crt', 'columna': 4, 'design': None},
				{'field_name': 'ws_archivo_key', 'columna': 4, 'design': None},
				{'field_name': 'ws_vence', 'columna': 2, 'design': None},
			],
			'fila_7': [
				{'field_name': 'ws_expiracion', 'columna': 2, 'design': None},
				{'field_name': 'ws_token', 'columna': 4, 'design': None},
				{'field_name': 'ws_sign', 'columna': 4, 'design': None},
			],
			'fila_8': [
				{'field_name': 'ws_modo', 'columna': 2, 'design': None},
			],
		},
		'Parámetros': {
			'fila_1': [
				{'field_name': 'interes', 'columna': 2, 'design': None},
				{'field_name': 'interes_dolar', 'columna': 2, 'design': None},
				{'field_name': 'cotizacion_dolar', 'columna': 2, 'design': None},
				{'field_name': 'dias_vencimiento', 'columna': 2, 'design': None},
				{'field_name': 'descuento_maximo', 'columna': 2, 'design': None},
			],
		},
	},

	'plan': {
		'Información Planes': {
			'fila_1': [
				{'field_name': 'estatus_plan', 'columna': 2, 'design': None},
				{'field_name': 'id_plan', 'columna': 2, 'design': None},
				{'field_name': 'descripcion_plan', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'cuota_plan', 'columna': 2, 'design': None},
				{'field_name': 'interes_plan', 'columna': 2, 'design': None},
				{'field_name': 'comision_plan', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'vigente_desde', 'columna': 2, 'design': None},
				{'field_name': 'vencimiento', 'columna': 2, 'design': None},
			],
		}
	},

	'plan_comercio': {
		'Información Planes de Comercios': {
			'fila_1': [
				{'field_name': 'estatus_plan_comercio', 'columna': 2, 'design': None},
			],
			'fila_2': [
				{'field_name': 'id_plan', 'columna': 4, 'design': None},
				{'field_name': 'id_comercio', 'columna': 4, 'design': None},
			],
		}
	},

	'solicitud_adhesion': {
		'Información Solicitud Adhesion Socios': {
			'fila_1': [
				{'field_name': 'estatus_solicitud_adhesion', 'columna': 2, 'design': None},
				{'field_name': 'id_socio', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'cuit_solicitud_adhesion', 'columna': 2, 'design': None},
				{'field_name': 'movil_solicitud_adhesion', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'email_solicitud_adhesion', 'columna': 4, 'design': None},
				{'field_name': 'estado_solicitud_adhesion', 'columna': 2, 'design': None},
			],
		}
	},

	'solicitud_vale': {
		'Solicitud Vales Socios': {
			'fila_1': [
				{'field_name': 'estatus_solicitud_vale', 'columna': 2, 'design': None},
			],
			'fila_2': [
				{'field_name': 'id_socio', 'columna': 3, 'design': None},
				{'field_name': 'id_comercio', 'columna': 3, 'design': None},
				{'field_name': 'monto_solicitud_vale', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'estado_solicitud_vale', 'columna': 2, 'design': None},
				{'field_name': 'limite_aprobado', 'columna': 2, 'design': None},
				{'field_name': 'fecha_aprobacion', 'columna': 2, 'design': None},
			],
			'fila_4': [
				{'field_name': 'observaciones', 'columna': 4, 'design': None},
			],
		}
	},

}
