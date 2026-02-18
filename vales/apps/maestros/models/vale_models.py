# vales\apps\maestros\models\vale_models.py
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date



from .base_gen_models import ModeloBaseGenerico
from .base_models import Plan
from .socio_models import Socio
from .comercio_models import Comercio
from entorno.constantes_base import (SOLICITUD_VALE, ESTATUS_GEN)

class SolicitudVale(ModeloBaseGenerico):
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
	consumido_solicitud_vale = models.DecimalField("Total Consumido", max_digits=15, 
									decimal_places=2, default=0.00)
	fecha_aprobacion = models.DateField("Fecha Aprobación", 
									null=True, blank=True)
	observaciones = models.CharField("Observaciones", max_length=200, 
									 null=True, blank=True)
	
	# Campos de seguridad de dispositivo
	device_id = models.CharField("ID Dispositivo", max_length=255,
								null=True, blank=True,
								help_text="Identificador único del dispositivo desde donde se solicitó el vale")
	device_model = models.CharField("Modelo Dispositivo", max_length=100,
							   null=True, blank=True)
	device_platform = models.CharField("Plataforma Dispositivo", max_length=20,
								  null=True, blank=True)
	
	class Meta:
		db_table = 'solicitud_vale'
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
				orig = SolicitudVale.objects.get(pk=self.pk)
				
				if orig.estado_solicitud_vale != 1:
					# No permitir modificaciones cuando el estado no es Pendiente
					raise ValidationError('No se puede modificar este registro porque ya fue cambiado su estado de Pendiente.')
				
				# 🔒 PRESERVAR device info del registro original al aprobar/rechazar
				# Si los campos device están vacíos pero el original los tenía, preservarlos
				if not self.device_id and orig.device_id:
					self.device_id = orig.device_id
					self.device_model = orig.device_model
					self.device_platform = orig.device_platform
					
			except SolicitudVale.DoesNotExist:
				orig = None

		# Lógica al cambiar estado
		# 2 -> Aprobado: guardar fecha y activar estatus
		if self.estado_solicitud_vale == 2:
			self.fecha_aprobacion = date.today()
			self.estatus_solicitud_vale = True
		# 3 -> Rechazado: limpiar límite aprobado y desactivar estatus
		elif self.estado_solicitud_vale == 3:
			self.limite_aprobado = 0.00
			self.estatus_solicitud_vale = False

		super(SolicitudVale, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.id_socio.nombre_socio} - {self.monto_solicitud_vale}"
	

class Compra(ModeloBaseGenerico):
	id_compra = models.AutoField(primary_key=True)
	estatus_compra = models.BooleanField("Estatus*", default=False, 
								choices=ESTATUS_GEN)
	id_solicitud_vale = models.ForeignKey(SolicitudVale, on_delete=models.CASCADE,
								null=False, blank=False,
								verbose_name="ID Vale*")
	id_socio = models.ForeignKey(Socio, on_delete=models.CASCADE,
								null=True, blank=True,
								verbose_name="Socio*")
	id_comercio = models.ForeignKey(Comercio, on_delete=models.CASCADE,
								null=True, blank=True,
								verbose_name="Comercio*")
	id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE,
								null=True, blank=True,
								verbose_name="Plan*")
	monto_compra = models.DecimalField("Monto Compra*", 
								max_digits=15, decimal_places=2,
								default=0.00)
	estado_compra = models.IntegerField("Estado Compra*", 
								default=1, choices=SOLICITUD_VALE)
	fecha_compra = models.DateField("Fecha Compra*", 
								null=True, blank=True)
	autorizacion_compra = models.IntegerField("Autorización Compra*", 
								default=0)
	idempotency_key = models.CharField("Idempotency Key", 
					max_length=36, null=True, blank=True, editable=False)
	
	# Campos de seguridad de dispositivo
	device_id = models.CharField("ID Dispositivo", max_length=255,
								null=True, blank=True,
								help_text="Identificador único del dispositivo desde donde se realizó la compra")
	device_model = models.CharField("Modelo Dispositivo", max_length=100,
							   null=True, blank=True)
	device_platform = models.CharField("Plataforma Dispositivo", max_length=20,
								  null=True, blank=True)

	class Meta:
		db_table = 'compra'
		verbose_name = ('Compra')
		verbose_name_plural = ('Compras')
		ordering = ['id_compra']
												
	def __str__(self):
		socio = self.id_socio.nombre_socio if self.id_socio else "Sin socio"
		return f"{socio} - {self.monto_compra}"


	def clean(self):
		super().clean()
		errors = {}
		# Validar que el socio esté activo
		if self.id_socio and not getattr(self.id_socio, 'estatus_socio', False):
			errors['id_socio'] = 'El socio seleccionado no está activo.'
		# Validar que el comercio esté activo
		if self.id_comercio and not getattr(self.id_comercio, 'estatus_comercio', False):
			errors['id_comercio'] = 'El comercio seleccionado no está activo.'
		# Validar que el plan esté activo
		if self.id_plan and not getattr(self.id_plan, 'estatus_plan', False):
			errors['id_plan'] = 'El plan seleccionado no está activo.'
		# Validar que el monto no exceda el saldo disponible del vale
		if self.id_solicitud_vale:
			saldo_disponible = self.id_solicitud_vale.limite_aprobado - self.id_solicitud_vale.consumido_solicitud_vale
			# Si estamos editando, descontar el monto anterior
			if self.pk:
				try:
					orig = Compra.objects.get(pk=self.pk)
					saldo_disponible += orig.monto_compra
				except Compra.DoesNotExist:
					pass
			
			if self.monto_compra > saldo_disponible:
				errors['monto_compra'] = f'El monto no puede exceder el saldo disponible ({saldo_disponible}).'
		
		if errors:
			raise ValidationError(errors)

	def save(self, *args, **kwargs):
		# Evitar modificaciones si el registro ya no está en estado Pendiente
		is_new = not self.pk
		orig = None
		
		if self.pk:
			try:
				orig = Compra.objects.get(pk=self.pk)
			except Compra.DoesNotExist:
				orig = None
			if orig and orig.estado_compra != 1:
				# No permitir modificaciones cuando el estado no es Pendiente
				raise ValidationError('No se puede modificar este registro porque ya fue cambiado su estado de Pendiente.')

		# Lógica al cambiar estado
		# 2 -> Aprobado: guardar fecha y activar estatus
		if self.estado_compra == 2 or self.estado_compra == 4:
			self.fecha_compra = date.today()
			self.estatus_compra = True
		# 3 -> Rechazado: Anula la compra y desactivar estatus
		elif self.estado_compra == 3:
			self.monto_compra = 0.00
			self.estatus_compra = False

		super(Compra, self).save(*args, **kwargs)
		
		# Actualizar el consumido_solicitud_vale del vale después de guardar
		if self.id_solicitud_vale:
			vale = self.id_solicitud_vale
			
			if is_new:
				# Nueva compra: sumar el monto al consumido
				vale.consumido_solicitud_vale += self.monto_compra
			else:
				# Editar compra: recalcular el consumido
				# Obtener la diferencia de monto
				if orig:
					diferencia = self.monto_compra - orig.monto_compra
					vale.consumido_solicitud_vale += diferencia
				else:
					vale.consumido_solicitud_vale += self.monto_compra
			
			# Asegurar que no sea negativo
			if vale.consumido_solicitud_vale < 0:
				vale.consumido_solicitud_vale = 0

			'''
			# Marcamos como 'Consumido' si se alcanza el importe
			if vale.consumido_solicitud_vale >= vale.limite_aprobado:
				vale.estado_solicitud_vale = 4 

			# Guardar el vale sin pasar por el save() para evitar validaciones
			SolicitudVale.objects.filter(pk=vale.pk).update(
				consumido_solicitud_vale=vale.consumido_solicitud_vale,
				estado_solicitud_vale=vale.estado_solicitud_vale
			)
			'''
			
			# Marcamos como 'Consumido' si se alcanza el importe
			vale_consumido = (vale.limite_aprobado > 0 and vale.consumido_solicitud_vale >= vale.limite_aprobado)
			if vale_consumido:
				vale.estado_solicitud_vale = 4

			# Guardar el vale sin pasar por el save() para evitar validaciones
			SolicitudVale.objects.filter(pk=vale.pk).update(
				consumido_solicitud_vale=vale.consumido_solicitud_vale,
				estado_solicitud_vale=vale.estado_solicitud_vale
			)

			# Si el vale quedó consumido, esta compra pasa a estado 4 (Consumido)
			if vale_consumido:
				Compra.objects.filter(pk=self.pk).update(
					estado_compra=4,
					estatus_compra=True,
					fecha_compra=date.today()
				)
				self.estado_compra = 4
				self.estatus_compra = True
				self.fecha_compra = date.today()
