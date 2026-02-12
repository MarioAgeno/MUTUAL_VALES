# vales\apps\maestros\admin.py
from django.contrib import admin

from .models.socio_models import Socio, SolicitudAdhesion
from .models.comercio_models import Comercio, PlanComercio
from .models.sucursal_models import Sucursal
from .models.vale_models import SolicitudVale, Compra
from .models.base_models import *
from .models.cuenta_comercio_models import CuentaComercio    

# Registramos los modelos independientes
admin.site.register(Socio)
admin.site.register(Comercio)
admin.site.register(Sucursal)
admin.site.register(PlanComercio)
admin.site.register(SolicitudAdhesion)
admin.site.register(SolicitudVale)
admin.site.register(Compra)

# Registramos los modelos base
admin.site.register(Servicio)
admin.site.register(Localidad)
admin.site.register(Provincia)
admin.site.register(TipoDocumentoIdentidad)
admin.site.register(TipoIva)
admin.site.register(Empresa)
admin.site.register(Parametro)
admin.site.register(Plan)

# Registar cuenta Comercio
@admin.register(CuentaComercio)
class CuentaComercioAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "comercio", "activo")
    search_fields = ("user__username", "user__email", "comercio__nombre_comercio")
    list_filter = ("activo",)

