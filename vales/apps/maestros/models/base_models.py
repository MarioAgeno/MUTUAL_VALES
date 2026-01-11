# vales\apps\maestros\models\base_models.py
from django.db import models
from django.utils.html import format_html
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from utils.validator.validaciones import validar_cuit
import re
from datetime import date

from .base_gen_models import ModeloBaseGenerico
from entorno.constantes_base import ESTATUS_GEN


class Servicio(ModeloBaseGenerico):
	id_servicio = models.AutoField(primary_key=True)
	estatus_servicio = models.BooleanField("Estatus", default=True,
											choices=ESTATUS_GEN)
	descripcion_servicio = models.CharField("Descripción servicio",
											 max_length=30)
	importe_servicio = models.DecimalField("Importe", max_digits=15, decimal_places=2,
							default=0.00, null=True, blank=True)
	gasto_fijo_servicio = models.DecimalField("Gasto Fijo $", max_digits=15, decimal_places=2,
							default=0.00, null=True, blank=True)
	gasto_porcentaje_servicio = models.DecimalField("Gastos en %", max_digits=6, 
							decimal_places=2, default=0.00,null=True, blank=True,
							validators=[MinValueValidator(0), MaxValueValidator(999.99)])
	numero_servicio = models.IntegerField("Numero", null=True, blank=True)
	cuota_servicio = models.IntegerField("Cuotas", null=True, blank=True,
							validators=[MinValueValidator(0), MaxValueValidator(99)])
	plan_servicio = models.IntegerField("Plan", null=True, blank=True,
							validators=[MinValueValidator(0), MaxValueValidator(99)])
	posterga_vencimiento = models.IntegerField("Postergar Vencimiento", null=True, blank=True,
							validators=[MinValueValidator(0), MaxValueValidator(9)])
	compro_servicio = models.CharField("Comprobante", max_length=6, default='')

	class Meta:
		db_table = 'servicio'
		verbose_name = ('Servicio')
		verbose_name_plural = ('Servicios')
		ordering = ['descripcion_servicio']

	def __str__(self):
		return self.descripcion_servicio


class Provincia(ModeloBaseGenerico):
	id_provincia = models.AutoField(primary_key=True)
	estatus_provincia = models.BooleanField("Estatus", default=True,
											choices=ESTATUS_GEN)
	codigo_provincia = models.CharField("Código", max_length=2, unique=True)
	nombre_provincia = models.CharField("Nombre", max_length=30)
	
	class Meta:
		db_table = 'provincia'
		verbose_name = ('Provincia')
		verbose_name_plural = ('Provincias')
		ordering = ['nombre_provincia']
	
	def __str__(self):
		return self.nombre_provincia


class Localidad(ModeloBaseGenerico):
	id_localidad = models.AutoField(primary_key=True)
	estatus_localidad = models.BooleanField("Estatus", default=True,
											choices=ESTATUS_GEN)
	nombre_localidad = models.CharField("Nombre Localidad", max_length=30)
	codigo_postal = models.CharField("Código Postal", max_length=5)
	id_provincia = models.ForeignKey('Provincia', on_delete=models.CASCADE,
									 verbose_name="Provincia")
	
	class Meta:
		db_table = 'localidad'
		verbose_name = ('Localidad')
		verbose_name_plural = ('Localidades')
		ordering = ['codigo_postal']
	
	def __str__(self):
		return self.nombre_localidad


class TipoDocumentoIdentidad(ModeloBaseGenerico):
	id_tipo_documento_identidad = models.AutoField(primary_key=True)
	estatus_tipo_documento_identidad = models.BooleanField("Estatus",
															 default=True,
															 choices=ESTATUS_GEN)
	nombre_documento_identidad = models.CharField("Nombre", max_length=20)
	tipo_documento_identidad = models.CharField("Tipo", max_length=4, 
												unique=True)
	codigo_afip = models.CharField("Código AFIP", max_length=2)
	ws_afip = models.CharField("WS AFIP", max_length=2)
	
	class Meta:
		db_table = 'tipo_documento_identidad'
		verbose_name = ('Tipo de Documento de Identidad')
		verbose_name_plural = ('Tipos de Documentos de Identidad')
		ordering = ['tipo_documento_identidad']
	
	def __str__(self):
		return self.nombre_documento_identidad


class TipoIva(ModeloBaseGenerico):
	id_tipo_iva = models.AutoField(primary_key=True)
	estatus_tipo_iva = models.BooleanField("Estatus", default=True,
											 choices=ESTATUS_GEN)
	codigo_iva = models.CharField("Código IVA", max_length=4, unique=True)
	nombre_iva = models.CharField("Nombre", max_length=25)
	discrimina_iva = models.BooleanField("Discrimina IVA", null=True,
										 blank=True)
	codigo_afip_responsable = models.IntegerField("Cód. AFIP", unique=True,
												  null=True, blank=True,
												  default=0)
	
	class Meta:
		db_table = 'tipo_iva'
		verbose_name = ('Tipo de IVA')
		verbose_name_plural = ('Tipos de IVA')
		ordering = ['nombre_iva']
	
	def __str__(self):
		return self.nombre_iva
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.codigo_iva.isupper():
			errors.update({'codigo_iva': 'Debe ingresar solo mayúsculas.'})
		
		if errors:
			raise ValidationError(errors)


class Empresa(ModeloBaseGenerico):
	id_empresa = models.AutoField(primary_key=True)
	estatus_empresa = models.BooleanField("Estatus*", default=True,
										  choices=ESTATUS_GEN)
	nombre_fiscal = models.CharField("Nombre Fiscal*", max_length=50)
	nombre_comercial = models.CharField("Nombre Comercial*", max_length=50)
	domicilio_empresa = models.CharField("Domicilio*", max_length=50)
	codigo_postal = models.CharField("Código postal*", max_length=4)
	id_localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, 
								  verbose_name="Localidad*")
	id_provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, 
								  verbose_name="Provincia*")
	id_iva = models.ForeignKey(TipoIva, on_delete=models.PROTECT, 
						 verbose_name="Tipo I.V.A.", null=True, blank=True)
	cuit = models.BigIntegerField("C.U.I.T.*", )
	ingresos_bruto = models.CharField("Ing. Bruto*", max_length=15)
	inicio_actividad = models.DateField("Inicio de actividad*")
	cbu = models.CharField("CBU Bancaria*", max_length=22)
	cbu_alias = models.CharField("CBU Alias*", max_length=50)
	cbu_vence = models.DateField("Vcto. CBU*")
	telefono = models.CharField("Teléfono*", max_length=20)
	email_empresa = models.EmailField("Correo*", max_length=50)
	web_empresa = models.CharField("Web", max_length=50, 
								   null=True, blank=True)
	logo_empresa = models.BinaryField()  # Para el campo 'image'

	class Meta:
		db_table = 'empresa'
		verbose_name = ('Empresa')
		verbose_name_plural = ('Empresas')
		ordering = ['nombre_fiscal']
	
	def __str__(self):
		return self.nombre_fiscal
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		try:
			validar_cuit(self.cuit)
		except ValidationError as e:
			errors['cuit'] = e.messages
		
		if not re.match(r'^\d{1,22}$', str(self.cbu)):
			errors.update({'cbu': 'Debe indicar sólo dígitos numéricos positivos, mínimo 1 y máximo 22.'})
		
		if not re.match(r'^\+?\d[\d ]{0,19}$', str(self.telefono)):
			errors.update({'telefono': 'Debe indicar sólo dígitos numéricos positivos, mínimo 1 y máximo 20, el signo + y espacios.'})
		
		if errors:
			raise ValidationError(errors)
	
	@property
	def cuit_formateado(self):
		cuit = str(self.cuit)
		return f"{cuit[:2]}-{cuit[2:-1]}-{cuit[-1:]}"


class Parametro(ModeloBaseGenerico):
	id_parametro = models.AutoField(primary_key=True)  # Clave primaria
	estatus_parametro = models.BooleanField("Estatus", default=True,
									choices=ESTATUS_GEN)  # Estatus del parámetro
	id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE,
								    verbose_name="Empresa")
	interes = models.DecimalField("Intereses(%)", max_digits=5,
									decimal_places=2, default=0.00, blank=True)
	fecha_vencimiento = models.DateField("Fecha Vencimiento", default=None,
                               		null=True, blank=True)

	
	class Meta:
		db_table = 'parametro'
		verbose_name = 'Parámetro'
		verbose_name_plural = 'Parámetros'
		ordering = ['id_empresa']
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		interes_str = str(self.interes) if self.interes is not None else ""
		
		if not re.match(r'^-?(0|[1-9]\d{0,1})(\.\d{1,2})?$', interes_str):
			errors.update({'interes': 'El valor debe ser un número negativo o positivo, con hasta 2 dígitos enteros y hasta 2 decimales o cero.'})
		
		if errors:
			raise ValidationError(errors)


class Plan(ModeloBaseGenerico):
	id_plan = models.AutoField(primary_key=True)
	estatus_plan = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)
	descripcion_plan = models.CharField("Descripción servicio", max_length=30)
	cuota_plan = models.IntegerField("Cuotas", null=True, blank=True,
							validators=[MinValueValidator(0), MaxValueValidator(99)])
	interes_plan = models.DecimalField("Interes", max_digits=6, decimal_places=2,
							default=0.00, null=True, blank=True,
							validators=[MinValueValidator(0), MaxValueValidator(999.99)])
	comision_plan = models.DecimalField("Comision", max_digits=6, decimal_places=2, 
							default=0.00, null=True, blank=True,
							validators=[MinValueValidator(0), MaxValueValidator(999.99)])
	vigente_desde = models.DateField("Vigente Desde", default=date.today, null=True, blank=True)
	vencimiento = models.DateField("Vencimiento", default=date.today, null=True, blank=True)

	class Meta:
		db_table = 'plan'
		verbose_name = ('Plan')
		verbose_name_plural = ('Planes')
		ordering = ['descripcion_plan']

	def __str__(self):
		return self.descripcion_plan


	
