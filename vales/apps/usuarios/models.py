# vales\apps\usuarios\models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from entorno.constantes_base import SI_NO

class User(AbstractUser):
	email = models.EmailField("Correo electrónico")
	email_alt = models.EmailField("Correo alternativo", max_length=50,
							   null=True, blank=True)
	telefono = models.CharField("Teléfono", max_length=15,
							 null=True, blank=True)
	iniciales = models.CharField("Iniciales", max_length=3,
								null=True, blank=True)
	id_sucursal = models.ForeignKey('maestros.Sucursal', 
								  on_delete=models.PROTECT,
								  null=True, blank=True,
								  verbose_name="Sucursal")
	
	# Campos de seguridad para identificación de dispositivo
	device_id = models.CharField("ID de Dispositivo", max_length=255,
							  null=True, blank=True,
							  help_text="Identificador único del dispositivo")
	device_model = models.CharField("Modelo de Dispositivo", max_length=255,
								 null=True, blank=True,
								 help_text="Marca y modelo del dispositivo")
	device_platform = models.CharField("Plataforma", max_length=50,
									null=True, blank=True,
									help_text="Sistema operativo (Android, iOS, etc.)")
	device_registered_at = models.DateTimeField("Fecha Registro Dispositivo",
											 null=True, blank=True,
											 help_text="Fecha de registro inicial del dispositivo")
	device_last_used_at = models.DateTimeField("Último Uso Dispositivo",
											null=True, blank=True,
											help_text="Última vez que se usó el dispositivo")


class DeviceRelinkRequest(models.Model):
	STATUS_PENDING = 'PENDING'
	STATUS_APPROVED = 'APPROVED'
	STATUS_REJECTED = 'REJECTED'

	STATUS_CHOICES = [
		(STATUS_PENDING, 'Pendiente'),
		(STATUS_APPROVED, 'Aprobada'),
		(STATUS_REJECTED, 'Rechazada'),
	]

	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='device_relink_requests',
		verbose_name='Usuario',
	)
	old_device_id = models.CharField(
		'Dispositivo Anterior',
		max_length=255,
		null=True,
		blank=True,
	)
	new_device_id = models.CharField('Nuevo Dispositivo', max_length=255)
	device_model = models.CharField('Modelo de Dispositivo', max_length=255, blank=True, default='')
	device_platform = models.CharField('Plataforma', max_length=50, blank=True, default='')
	status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	requested_at = models.DateTimeField('Fecha Solicitud', auto_now_add=True)
	resolved_at = models.DateTimeField('Fecha Resolución', null=True, blank=True)
	request_ip = models.GenericIPAddressField('IP Solicitud', null=True, blank=True)
	user_agent = models.TextField('User Agent', blank=True, default='')
	resolution_notes = models.TextField('Notas Resolución', blank=True, default='')

	class Meta:
		verbose_name = 'Solicitud de Re-vinculación'
		verbose_name_plural = 'Solicitudes de Re-vinculación'
		ordering = ['-requested_at']
		constraints = [
			models.UniqueConstraint(
				fields=['user'],
				condition=Q(status='PENDING'),
				name='unique_pending_device_relink_per_user',
			)
		]

	def __str__(self):
		return f'{self.user.username} - {self.status} - {self.requested_at:%Y-%m-%d %H:%M}'


# -- Al crear un nuevo usuario este quede activo por defecto.
@receiver(post_save, sender=User)
def set_user_active(sender, instance, created, **kwargs):
	if created and not instance.is_active:
		instance.is_active = True
		instance.save()
		
