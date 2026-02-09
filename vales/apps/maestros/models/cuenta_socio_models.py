from django.conf import settings
from django.db import models
from django.utils import timezone

from .socio_models import Socio

class CuentaSocio(models.Model):
    socio = models.OneToOneField(
        Socio,
        on_delete=models.PROTECT,
        related_name="cuenta_acceso",
        db_index=True,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cuenta_socio",
        db_index=True,
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "cuenta_socio"
        verbose_name = "Cuenta Socio"
        verbose_name_plural = "Cuentas Socios"

    def __str__(self):
        return f"{self.socio} -> {self.user}"
