from django.conf import settings
from django.db import models

from .comercio_models import Comercio 

class CuentaComercio(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cuenta_comercio",
        verbose_name="Usuario"
    )
    comercio = models.ForeignKey(
        Comercio,
        on_delete=models.CASCADE,
        related_name="cuentas",
        verbose_name="Comercio"
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "cuenta_comercio"
        verbose_name = "Cuenta Comercio"
        verbose_name_plural = "Cuentas Comercio"

    def __str__(self):
        return f"{self.comercio_id} - {self.user_id}"
