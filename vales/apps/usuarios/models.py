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


# -- Al crear un nuevo usuario este quede activo por defecto.
@receiver(post_save, sender=User)
def set_user_active(sender, instance, created, **kwargs):
	if created and not instance.is_active:
		instance.is_active = True
		instance.save()
		
