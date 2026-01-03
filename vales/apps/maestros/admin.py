# vales\apps\maestros\admin.py
from django.contrib import admin

from .models.socio_models import Socio, SolicitudAdhesion
from .models.comercio_models import Comercio, PlanComercio
from .models.sucursal_models import Sucursal
from .models.vale_models import SolcitudVale, Vale
from .models.base_models import *

# Registramos los modelos independientes
admin.site.register(Socio)
admin.site.register(Comercio)
admin.site.register(Sucursal)
admin.site.register(PlanComercio)
admin.site.register(SolicitudAdhesion)
admin.site.register(SolcitudVale)
admin.site.register(Vale)

# Registramos los modelos base
admin.site.register(Servicio)
admin.site.register(Localidad)
admin.site.register(Provincia)
admin.site.register(TipoDocumentoIdentidad)
admin.site.register(TipoIva)
admin.site.register(Empresa)
admin.site.register(Parametro)
admin.site.register(Plan)

