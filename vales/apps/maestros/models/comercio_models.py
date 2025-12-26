# vales\apps\maestros\models\comercio_models.py
from django.db import models
from django.core.exceptions import ValidationError
import re

from utils.validator.validaciones import validar_cuit
from .base_gen_models import ModeloBaseGenerico
from .base_models import Provincia, Localidad, TipoIva, Servicio, Plan
from entorno.constantes_base import ESTATUS_GEN, PAGO_COMERCIO
from django.core.validators import MinValueValidator, MaxValueValidator


class Comercio(ModeloBaseGenerico):
	id_comercio = models.AutoField(primary_key=True)
	estatus_comercio = models.BooleanField("Estatus", default=True, 
										 choices=ESTATUS_GEN)
	nombre_comercio = models.CharField("Nombre Comercio", max_length=50)
	domicilio_comercio = models.CharField("Domicilio", max_length=50,
										 blank=True, null=True)
	codigo_postal = models.CharField("Código Postal*", max_length=5,
								  blank=True, null=True)
	id_provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, 
									 verbose_name="Provincia*",
									 blank=True, null=True)
	id_localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT,
									 verbose_name="Localidad*",
									 blank=True, null=True)
	id_tipo_iva = models.ForeignKey(TipoIva, on_delete=models.PROTECT, 
								 verbose_name="Tipo IVA",
								 blank=True, null=True)
	cuit = models.IntegerField("C.U.I.T.", unique=True)
	telefono_comercio = models.CharField("Teléfono", max_length=15)
	movil_comercio = models.CharField("Móvil", max_length=15, 
										null=True, blank=True)
	email_comercio = models.EmailField("Correo", max_length=50,
									 blank=True, null=True)
	id_servicio = models.ForeignKey(Servicio, 
									on_delete=models.PROTECT,
									null=True, blank=True,
									verbose_name="Servicio*")
	pago = models.IntegerField("Forma de Pago*", 
										  default=1,
										  choices=PAGO_COMERCIO)
	bonificacion_comercio = models.DecimalField("Bonificación en %", max_digits=6, 
							decimal_places=2, default=0.00,null=True, blank=True,
							validators=[MinValueValidator(0), MaxValueValidator(999.99)])
	gasto_adm_comercio = models.DecimalField("Gastos en %", max_digits=6, 
							decimal_places=2, default=0.00,null=True, blank=True,
							validators=[MinValueValidator(0), MaxValueValidator(999.99)])
	
	observacion_comercio = models.TextField("Observaciones", blank=True, 
											null=True)

	class Meta:
		db_table = 'comercio'
		verbose_name = 'Comercio'
		verbose_name_plural = 'Comercios'
		ordering = ['nombre_comercio']
	
	def __str__(self):
		return f'{self.nombre_comercio} - {self.cuit}'
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		try:
			validar_cuit(self.cuit)
		except ValidationError as e:
			errors['cuit'] = e.messages
		
		if not re.match(r'^\+?\d[\d ]{0,14}$', str(self.telefono_comercio)):
			errors.update({'telefono_comercio': 'Debe indicar sólo dígitos numéricos positivos, mínimo 1 y máximo 15, el signo + y espacios.'})
		
		if self.movil_comercio and not re.match(r'^\+?\d[\d ]{0,14}$', str(self.movil_comercio)):
			errors.update({'movil_comercio': 'Debe indicar sólo dígitos numéricos positivos, mínimo 1 y máximo 15, el signo +, espacios o vacío.'})
		
		if errors:
			raise ValidationError(errors)
	
	@property
	def cuit_formateado(self):
		cuit = str(self.cuit)
		return f"{cuit[:2]}-{cuit[2:-1]}-{cuit[-1:]}"


class PlanComercio(ModeloBaseGenerico):
	id_plan_comercio = models.AutoField(primary_key=True)
	estatus_plan_comercio = models.BooleanField("Estatus*", default=True,
										  choices=ESTATUS_GEN)
	id_plan = models.ForeignKey(Plan, on_delete=models.PROTECT, 
								  verbose_name="Plan*")
	id_comercio = models.ForeignKey(Comercio, on_delete=models.PROTECT, 
								  verbose_name="Comercio*")
	class Meta:
		db_table = 'plan_comercio'
		verbose_name = ('Plan Comercio')
		verbose_name_plural = ('Planes Comercios')
		ordering = ['id_plan']
	
	def __str__(self):
		return self.id_plan.descripcion_plan