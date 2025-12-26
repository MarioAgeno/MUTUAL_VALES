# neumatic\entorno\constantes_base.py

# -- Datos estándares aplicables a los modelos base
ESTATUS_GEN = [
	(True, 'Activo'),
	(False, 'Inactivo'),
]

TIPO_PERSONA = [
	("F", 'Física'),
	("J", 'Jurídica'),
]

PAGO_COMERCIO = [
	(1, 'Contado'),
	(2, 'Cuotas'),
]

SEXO = [
	("M", 'Masculino'),
	("F", 'Femenino'),
]

SI_NO = [
	(True, 'SI'),
	(False, 'NO')
]

MESES = [
		('01', 'Enero'),
		('02', 'Febrero'),
		('03', 'Marzo'),
		('04', 'Abril'),
		('05', 'Mayo'),
		('06', 'Junio'),
		('07', 'Julio'),
		('08', 'Agosto'),
		('09', 'Septiembre'),
		('10', 'Octubre'),
		('11', 'Noviembre'),
		('12', 'Diciembre'),
	]

SOLICITUD_SOCIO = [
	(1, 'Pendiente'),
	(2, 'Aprobada'),
	(3, 'Rechazada'),
]

SOLICITUD_VALE = [
	(1, 'Pendiente'),
	(2, 'Aprobado'),
	(3, 'Rechazado'),
    (4, 'Consumido'),
]