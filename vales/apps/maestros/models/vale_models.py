# vales\apps\maestros\models\vale_models.py
from django.db import models
from django.core.exceptions import ValidationError
import re
from datetime import date

from .base_gen_models import ModeloBaseGenerico
from .socio_models import Socio
from .comercio_models import Comercio
from entorno.constantes_base import (SOLICITUD_VALE, ESTATUS_GEN)

class SolcitudVale(ModeloBaseGenerico):
	id_solicitud_vale = models.AutoField(primary_key=True)
	estatus_solicitud_vale = models.BooleanField("Estatus*", default=False, 
										  choices=ESTATUS_GEN)
	id_socio = models.ForeignKey(Socio, on_delete=models.CASCADE,
									null=True, blank=True,
									verbose_name="Socio*")
	id_comercio = models.ForeignKey(Comercio, on_delete=models.CASCADE,
									null=True, blank=True,
									verbose_name="Comercio*")
	monto_solicitud_vale = models.DecimalField("Monto Solicitud Vale", 
										 max_digits=15, decimal_places=2,
										 default=0.00)
	estado_solicitud_vale = models.IntegerField("Estado Solicitud Vale*", 
										 default=1, choices=SOLICITUD_VALE)
	limite_aprobado = models.DecimalField("Límite Aprobado", max_digits=15, 
									     decimal_places=2, default=0.00)
	fecha_aprobacion = models.DateField("Fecha Aprobación", 
									 null=True, blank=True)
	observaciones = models.CharField("Observaciones", max_length=200, 
									 null=True, blank=True)
	
	class Meta:
		db_table = 'vale'
		verbose_name = ('Solicitud Vale')
		verbose_name_plural = ('Solicitudes de Vales')
		ordering = ['id_solicitud_vale']
												

	def clean(self):
		super().clean()
		errors = {}
		# Validar que el socio esté activo
		if self.id_socio and not getattr(self.id_socio, 'estatus_socio', False):
			errors['id_socio'] = 'El socio seleccionado no está activo.'
		# Validar que el comercio esté activo
		if self.id_comercio and not getattr(self.id_comercio, 'estatus_comercio', False):
			errors['id_comercio'] = 'El comercio seleccionado no está activo.'
		if errors:
			raise ValidationError(errors)

	def save(self, *args, **kwargs):
		# Evitar modificaciones si el registro ya no está en estado Pendiente
		if self.pk:
			try:
				orig = SolcitudVale.objects.get(pk=self.pk)
			except SolcitudVale.DoesNotExist:
				orig = None
			if orig and orig.estado_solicitud_vale != 1:
				# No permitir modificaciones cuando el estado no es Pendiente
				raise ValidationError('No se puede modificar este registro porque su estado no es Pendiente.')

		# Lógica al cambiar estado
		# 2 -> Aprobado: guardar fecha y activar estatus
		if self.estado_solicitud_vale == 2:
			self.fecha_aprobacion = date.today()
			self.estatus_solicitud_vale = True
		# 3 -> Rechazado: limpiar límite aprobado y desactivar estatus
		elif self.estado_solicitud_vale == 3:
			self.limite_aprobado = 0.00
			self.estatus_solicitud_vale = False

		super(SolcitudVale, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.id_socio.nombre_socio} - {self.monto_solicitud_vale}"
	