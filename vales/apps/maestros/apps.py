# vales\apps\maestros\apps.py
from django.apps import AppConfig


class MaestrosConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'apps.maestros'
	
	def ready(self):
		import apps.maestros.models.base_gen_models
		import apps.maestros.models.base_models
		import apps.maestros.models.socio_models
		import apps.maestros.models.comercio_models
		import apps.maestros.models.sucursal_models
		import apps.maestros.models.valida_models
