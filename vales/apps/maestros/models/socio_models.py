# vales\apps\maestros\models\cliente_models.py
from django.db import models
from django.core.exceptions import ValidationError
import re
from datetime import date

from utils.validator.validaciones import validar_cuit
from .base_gen_models import ModeloBaseGenerico
from .base_models import (Localidad, Provincia, TipoIva, 
						  TipoDocumentoIdentidad)
from .sucursal_models import Sucursal
from entorno.constantes_base import (SOLICITUD_SOCIO,
	ESTATUS_GEN, SEXO, TIPO_PERSONA, SI_NO)

class Socio(ModeloBaseGenerico):
	id_socio = models.AutoField(primary_key=True)
	estatus_socio = models.BooleanField("Estatus*", default=False, 
									choices=ESTATUS_GEN)
	codigo_socio = models.IntegerField("Código", null=True, blank=True)
	nombre_socio = models.CharField("Nombre Socio*", max_length=50)
	domicilio_socio = models.CharField("Domicilio Socio*", max_length=50)
	codigo_postal = models.CharField("Código Postal*", max_length=5,
                                    null=True, blank=True)
	id_provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, 
									verbose_name="Provincia*",
          							null=True, blank=True)
	id_localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT,
									verbose_name="Localidad*",
         							null=True, blank=True)
	tipo_persona = models.CharField("Tipo de Persona*", max_length=1,
									default="F", 
									choices=TIPO_PERSONA)
	id_tipo_iva = models.ForeignKey(TipoIva, on_delete=models.PROTECT,
									verbose_name="Tipo de IVA*")
	id_tipo_documento_identidad = models.ForeignKey(TipoDocumentoIdentidad, 
									on_delete=models.PROTECT, 
									verbose_name="Tipo Doc. Identidad*")
	numero_documento = models.IntegerField("Número doc.*", null=True, blank=True)
	cuit = models.BigIntegerField("CUIT/CUIL*", unique=True, null=True, blank=True)
	legajo = models.BigIntegerField("Legajo*", unique=True, null=True, blank=True)
	telefono_socio = models.CharField("Teléfono*", max_length=15)
	telefono2_socio = models.CharField("Teléfono Alternativo", max_length=15,
									null=True, blank=True)
	movil_socio = models.CharField("Móvil", max_length=15, null=True, blank=True)
	email_socio = models.EmailField("Email*", max_length=50)
	fecha_nacimiento = models.DateField("Fecha Nacimiento", 
									null=True, blank=True)
	fecha_alta = models.DateField("Fecha Alta", default=date.today,
                               		null=True, blank=True)
	sexo = models.CharField("Sexo*", max_length=1, 
									default="M", choices=SEXO)
	id_sucursal = models.ForeignKey(Sucursal, 
									on_delete=models.CASCADE,
									null=True, blank=True,
									verbose_name="Sucursal*")
	black_list = models.BooleanField("Black List", default=False, 
									 choices=SI_NO)
	black_list_motivo = models.CharField("Motivo Black List", max_length=50, 
									  null=True, blank=True)
	black_list_usuario = models.CharField("Usuario Black List", 
									 max_length=20, null=True, blank=True)
	fecha_baja = models.DateField("Fecha de Baja", null=True, blank=True)
	class Meta:
		db_table = 'socio'
		verbose_name = ('Socio')
		verbose_name_plural = ('Socios')
		ordering = ['nombre_socio']
												
	def __str__(self):
		return self.nombre_socio
	
	def clean(self):
		super().clean()
		
		#-- Diccionario contenedor de errores.
		errors = {}
		
		#-- Convertir a string los valores de los campos previo a la validación.
		telefono_str = str(self.telefono_socio) if self.telefono_socio else ''
		movil_socio_str = str(self.movil_socio) if self.movil_socio else ''

		try:
			validar_cuit(self.cuit)
		except ValidationError as e:
			errors['cuit'] = e.messages
	
		if not self.cuit:
			errors.update({'cuit': 'Debe indicar un Número de CUIT / CUIL'})
		
		if not self.numero_documento:
			errors.update({'numero_documento': 'Debe indicar un Número de Documento de Identidad.'})

		if not re.match(r'^\+?\d[\d ]{0,14}$', telefono_str):
			errors.update({'telefono_socio': 'Debe indicar sólo dígitos numéricos positivos, \
       			mínimo 1 y máximo 15, el signo + y espacios.'})
		
		if movil_socio_str and not re.match(r'^\+?\d[\d ]{0,14}$', movil_socio_str):
			errors.update({'movil_socio': 'Debe indicar sólo dígitos numéricos positivos, mínimo 1 y máximo 15, el signo +, espacios o vacío.'})
			
		if errors:
			#-- Lanza el conjunto de excepciones.
			raise ValidationError(errors)
	
	@property
	def cuit_formateado(self):
		cuit = str(self.cuit)
		if self.nombre_tipo_documento_identidad.lower() == "cuit":
			cuit = f"{cuit[:2]}-{cuit[2:-1]}-{cuit[-1:]}"
		return cuit
	
	@property
	def nombre_tipo_documento_identidad(self):
		return self.id_tipo_documento_identidad.nombre_documento_identidad
	

class SolicitudAdhesion(ModeloBaseGenerico):
	id_solicitud_adhesion = models.AutoField(primary_key=True)
	estatus_solicitud_adhesion = models.BooleanField(
									"Estatus*", default=True, 
									choices=ESTATUS_GEN)
	id_socio = models.ForeignKey(Socio, on_delete=models.CASCADE,
									verbose_name="Socio*")
	nombre_solicitud_adhesion = models.CharField("Nombre Socio*", max_length=50,
									null=True, blank=True)
	cuit_solicitud_adhesion = models.BigIntegerField("CUIT/CUIL*", 
									null=True, blank=True)
	legajo_solicitud_adhesion = models.BigIntegerField("Legajo*", 
									null=True, blank=True)
	movil_solicitud_adhesion = models.CharField("Móvil*", max_length=15, 
									null=True, blank=True)
	email_solicitud_adhesion = models.EmailField("Email*", max_length=50,
									null=True, blank=True)
	estado_solicitud_adhesion = models.IntegerField("Estado Solicitud Adhesión*", 
									default=1,
									choices=SOLICITUD_SOCIO)

	class Meta:
		db_table = 'solicitud_adhesion'
		verbose_name = ('Solicitud de Adhesión')
		verbose_name_plural = ('Solicitudes de Adhesión')
		ordering = ['id_socio']

	def save(self, *args, **kwargs):
		# Verificar si el estado cambió a Aprobada (2)
		if self.estado_solicitud_adhesion == 2:
			self.estatus_solicitud_adhesion = True
			socio = self.id_socio
			socio.estatus_socio = True
			if self.movil_solicitud_adhesion:
				socio.movil_socio = self.movil_solicitud_adhesion
			if self.email_solicitud_adhesion:
				socio.email_socio = self.email_solicitud_adhesion
			socio.save()
		super().save(*args, **kwargs)
