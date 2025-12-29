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
												
	def __str__(self):
		return self.id_socio.nombre_socio + " - " + str(self.monto_solicitud_vale)
	