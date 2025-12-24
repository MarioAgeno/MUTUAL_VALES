# vales\apps\maestros\admin.py
from django.contrib import admin

from .models.socio_models import Socio
from .models.comercio_models import Comercio
from .models.sucursal_models import Sucursal
from .models.base_models import *

# Registramos los modelos independientes
admin.site.register(Socio)
admin.site.register(Empresa)
admin.site.register(Parametro)
admin.site.register(Comercio)
admin.site.register(Sucursal)

# Registramos los modelos base
admin.site.register(Servicio)
admin.site.register(Localidad)
admin.site.register(Provincia)
admin.site.register(TipoDocumentoIdentidad)
admin.site.register(TipoIva)
