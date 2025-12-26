# vales\apps\maestros\views\plan_views.py
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from .cruds_views_generics import *
from ..models.base_models import Plan
from ..models.comercio_models import PlanComercio, Comercio
from ..forms.plan_forms_base import PlanForm


class ConfigViews():
	#-- Modelo.
	model = Plan
	
	#-- Formulario asociado al modelo.
	form_class = PlanForm
	
	#-- Aplicación asociada al modelo.
	app_label = model._meta.app_label
	
	#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	model_string = model.__name__.lower()  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	
	#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
	#model_string = "tipo_cambio"
	
	#-- Permisos.
	permission_add = f"{app_label}.add_{model.__name__.lower()}"
	permission_change = f"{app_label}.change_{model.__name__.lower()}"
	permission_delete = f"{app_label}.delete_{model.__name__.lower()}"
	
	#-- Vistas del CRUD del modelo.
	list_view_name = f"{model_string}_list"
	create_view_name = f"{model_string}_create"
	update_view_name = f"{model_string}_update"
	delete_view_name = f"{model_string}_delete"
	
	#-- Plantilla para crear o actualizar el modelo.
	template_form = f"{app_label}/{model_string}_form.html"
	
	#-- Plantilla para confirmar eliminación de un registro.
	template_delete = "base_confirm_delete.html"
	
	#-- Plantilla de la lista del CRUD.
	template_list = f'{app_label}/maestro_list.html'
	
	#-- Contexto de los datos de la lista.
	context_object_name	= 'objetos'
	
	#-- Vista del home del proyecto.
	home_view_name = "home"
	
	#-- Nombre de la url.
	success_url = reverse_lazy(list_view_name)


class DataViewList():
	search_fields = ['descripcion_plan']
	
	ordering = ['descripcion_plan']
	
	paginate_by = 8
	  
	table_headers = {
		'estatus_plan': (1, 'Estatus'),
		'id_plan': (1, 'ID'),
		'descripcion_plan': (4, 'Descripción'),
		'cuota_plan': (1, 'Cuotas'),
		'interes_plan': (2, 'Interes'),
		'comision_plan': (2, 'Comision'),
		'acciones': (1, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_plan', 'date_format': None},
		{'field_name': 'id_plan', 'date_format': None},
		{'field_name': 'descripcion_plan', 'date_format': None},
		{'field_name': 'cuota_plan', 'date_format': None},
		{'field_name': 'interes_plan', 'date_format': 'percentage'},
		{'field_name': 'comision_plan', 'date_format': 'percentage'},
	]

class PlanListView(MaestroListView):
	model = ConfigViews.model
	template_name = ConfigViews.template_list
	context_object_name = ConfigViews.context_object_name
	
	search_fields = DataViewList.search_fields
	ordering = DataViewList.ordering
	
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


class PlanCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class PlanUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class PlanDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete



class PlanAsignarATodosView(MaestroCustomView):
	"""Asigna el plan a todos los comercios activos (sin duplicar)."""
	permission_required = ConfigViews.permission_change
	list_view_name = ConfigViews.list_view_name
	
	def post(self, request, pk, *args, **kwargs):
		plan = get_object_or_404(Plan, pk=pk)
		try:
			with transaction.atomic():
				comercios = Comercio.objects.filter(estatus_comercio=True)
				created_count = 0
				for c in comercios:
					obj, created = PlanComercio.objects.get_or_create(
						id_plan=plan,
						id_comercio=c,
						defaults={'estatus_plan_comercio': True}
					)
					if created:
						created_count += 1
				message = f"{created_count} planes asignados. {comercios.count()-created_count} ya existían."
				# Si es AJAX, devolver JSON para que el cliente lo maneje
				if request.headers.get('x-requested-with') == 'XMLHttpRequest':
					return JsonResponse({
						'success': True,
						'created': created_count,
						'existing': comercios.count() - created_count,
						'message': message,
					})
				else:
					messages.success(request, message)
		except Exception as e:
			# Manejo de error para AJAX o petición normal
			if request.headers.get('x-requested-with') == 'XMLHttpRequest':
				return JsonResponse({'success': False, 'message': f'Ocurrió un error al asignar: {e}'} , status=500)
			else:
				messages.error(request, f"Ocurrió un error al asignar: {e}")
				return redirect('plan_update', pk=pk)

		# Si no fue AJAX, redirigir al formulario de edición
		return redirect('plan_update', pk=pk)
