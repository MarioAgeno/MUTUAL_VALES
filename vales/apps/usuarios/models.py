# vales\apps\usuarios\models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
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


# -- Al crear un nuevo usuario este quede activo por defecto.
@receiver(post_save, sender=User)
def set_user_active(sender, instance, created, **kwargs):
	if created and not instance.is_active:
		instance.is_active = True
		instance.save()
		
