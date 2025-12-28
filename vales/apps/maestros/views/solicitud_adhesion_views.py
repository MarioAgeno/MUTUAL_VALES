# vales\apps\maestros\views\solicitud_adhesion_views.py
from django.urls import reverse_lazy
from .cruds_views_generics import *
from ..models.socio_models import SolicitudAdhesion
from ..forms.solicitud_adhesion_forms import SolicitudAdhesionForm
from entorno.constantes_base import SOLICITUD_SOCIO


class ConfigViews():
	# Modelo
	model = SolicitudAdhesion
	
	# Formulario asociado al modelo
	form_class = SolicitudAdhesionForm
	
	# Aplicación asociada al modelo
	app_label = model._meta.app_label
	
	#-- Deshabilitado por redundancia:
	# # Título del listado del modelo
	# master_title = model._meta.verbose_name_plural
	
	#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	# model_string = model.__name__.lower()  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	
	#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
	model_string = "solicitud_adhesion" 
	
	# Permisos
	permission_add = f"{app_label}.add_{model.__name__.lower()}"
	permission_change = f"{app_label}.change_{model.__name__.lower()}"
	permission_delete = f"{app_label}.delete_{model.__name__.lower()}"
	
	# Vistas del CRUD del modelo
	list_view_name = f"{model_string}_list"
	create_view_name = f"{model_string}_create"
	update_view_name = f"{model_string}_update"
	delete_view_name = f"{model_string}_delete"
	
	# Plantilla para crear o actualizar el modelo
	template_form = f"{app_label}/{model_string}_form.html"
	
	# Plantilla para confirmar eliminación de un registro
	template_delete = "base_confirm_delete.html"
	
	# Plantilla de la lista del CRUD
	template_list = f'{app_label}/maestro_list.html'
	
	# Contexto de los datos de la lista
	context_object_name	= 'objetos'
	
	# Vista del home del proyecto
	home_view_name = "home"
	
	# Nombre de la url 
	success_url = reverse_lazy(list_view_name)


class DataViewList():
	search_fields = ['id_socio__nombre_socio', 'cuit_solicitud_adhesion']

	# Ordenar por el nombre del comercio y por la descripción del plan
	ordering = ['id_socio__nombre_socio', 'cuit_solicitud_adhesion']

	paginate_by = 8
	
	table_headers = {
		'estatus_solicitud_adhesion': (1, 'Estatus'),
		'id_solicitud_adhesion': (1, 'ID Solicitud'),
		'id_socio': (3, 'Nombre Socio'),
		'cuit_solicitud_adhesion': (2, 'CUIT/CUIL'),
		'movil_solicitud_adhesion': (2, 'Teléfono Móvil'),
		'estado_solicitud_adhesion': (2, 'Estado Solicitud'),
		'acciones': (1, 'Acciones'),
	}

	table_data = [
		{'field_name': 'estatus_solicitud_adhesion', 'date_format': None},
		{'field_name': 'id_solicitud_adhesion', 'date_format': None},
		{'field_name': 'id_socio', 'date_format': None},
		{'field_name': 'cuit_solicitud_adhesion', 'date_format': None},
		{'field_name': 'movil_solicitud_adhesion', 'date_format': None},
		{'field_name': 'estado_solicitud_adhesion', 'date_format': None},
	]


# SolicitudAdhesionListView - Inicio
class SolicitudAdhesionListView(MaestroListView):
	model = ConfigViews.model
	template_name = ConfigViews.template_list
	context_object_name = ConfigViews.context_object_name
	
	search_fields = DataViewList.search_fields
	ordering = DataViewList.ordering
	
	def get_queryset(self):
		queryset = self.model.objects.all()
		
		# Obtener el valor de búsqueda
		query = self.request.GET.get('busqueda', None)
		
		if query:
			# Crear diccionario inverso para mapear texto a valor
			estado_dict = {display.lower(): value for value, display in SOLICITUD_SOCIO}
			
			# Dividir la query en palabras
			palabras = query.lower().split()
			
			# Buscar si alguna palabra coincide parcialmente con un estado
			estado_filtrar = None
			palabras_busqueda = []
			for palabra in palabras:
				estado_encontrado = None
				for value, display in SOLICITUD_SOCIO:
					if len(palabra) >= 3 and display.lower().startswith(palabra):
						estado_encontrado = value
						break
				if estado_encontrado is not None:
					estado_filtrar = estado_encontrado
				else:
					palabras_busqueda.append(palabra)
			
			# Aplicar filtro de estado si se encontró
			if estado_filtrar is not None:
				queryset = queryset.filter(estado_solicitud_adhesion=estado_filtrar)
			
			# Aplicar búsqueda en otros campos con las palabras restantes
			if palabras_busqueda:
				from django.db.models import Q
				busqueda_texto = ' '.join(palabras_busqueda)
				search_conditions = Q()
				for field in self.search_fields:
					search_conditions |= Q(**{f"{field}__icontains": busqueda_texto})
				queryset = queryset.filter(search_conditions)
		
		return queryset.order_by(*self.ordering)
	
	extra_context = {
		"master_title": ConfigViews.model._meta.verbose_name_plural,
		"home_view_name": ConfigViews.home_view_name,
		"list_view_name": ConfigViews.list_view_name,
		"create_view_name": ConfigViews.create_view_name,
		"update_view_name": ConfigViews.update_view_name,
		"delete_view_name": ConfigViews.delete_view_name,
		"table_headers": DataViewList.table_headers,
		"table_data": DataViewList.table_data,
	}


# SolicitudAdhesionCreateView - Inicio
class SolicitudAdhesionCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	# (revisar de donde lo copiaste que tienes asignado permission_change en vez de permission_add)
	permission_required = ConfigViews.permission_add
	
	# extra_context = {
	# 	"accion": f"Crear {ConfigViews.model._meta.verbose_name}",
	# 	"list_view_name" : ConfigViews.list_view_name
	# }


# SolicitudAdhesionUpdateView
class SolicitudAdhesionUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change
	
	# extra_context = {
	# 	"accion": f"Editar {ConfigViews.model._meta.verbose_name}",
	# 	"list_view_name" : ConfigViews.list_view_name
	# }


# SolicitudAdhesionDeleteView
class SolicitudAdhesionDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete
	
	# extra_context = {
	# 	"accion": f"Eliminar {ConfigViews.model._meta.verbose_name}",
	# 	"list_view_name" : ConfigViews.list_view_name,
	# 	"mensaje": "Estás seguro de eliminar el Registro"
	# }
