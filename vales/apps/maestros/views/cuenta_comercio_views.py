from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView

from .cruds_views_generics import MaestroListView
from ..forms.cuenta_comercio_forms import CuentaComercioCreateForm, CuentaComercioUpdateForm
from ..models.cuenta_comercio_models import CuentaComercio


User = get_user_model()


def _asignar_grupo_comercio(user):
	"""Asegura que el usuario vinculado a comercio pertenezca al grupo Comercio."""
	grupo_comercio, _ = Group.objects.get_or_create(name='Comercio')
	user.groups.add(grupo_comercio)


class StaffRequiredMixin(LoginRequiredMixin):
	login_url = reverse_lazy('iniciar_sesion')

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff and not request.user.is_superuser:
			messages.error(request, 'No tienes permisos para gestionar Cuentas Comercio.')
			return redirect('home')
		return super().dispatch(request, *args, **kwargs)


class CuentaComercioListView(StaffRequiredMixin, MaestroListView):
	model = CuentaComercio
	template_name = 'maestros/maestro_list.html'
	context_object_name = 'objetos'
	search_fields = [
		'user__username',
		'user__email',
		'comercio__nombre_comercio',
	]
	ordering = ['comercio__nombre_comercio', 'user__username']

	extra_context = {
		'master_title': 'Cuentas Comercio',
		'home_view_name': 'home',
		'list_view_name': 'cuenta_comercio_list',
		'create_view_name': 'cuenta_comercio_create',
		'update_view_name': 'cuenta_comercio_update',
		'delete_view_name': 'cuenta_comercio_delete',
		'table_headers': {
			'user': (3, 'Usuario'),
			'comercio': (4, 'Comercio'),
			'activo': (1, 'Activo'),
			'acciones': (2, 'Acciones'),
		},
		'table_data': [
			{'field_name': 'user', 'date_format': None},
			{'field_name': 'comercio', 'date_format': None},
			{'field_name': 'activo', 'date_format': None},
		],
	}


class CuentaComercioCreateView(StaffRequiredMixin, CreateView):
	model = CuentaComercio
	form_class = CuentaComercioCreateForm
	template_name = 'maestros/cuenta_comercio_form.html'
	success_url = reverse_lazy('cuenta_comercio_list')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['current_user'] = self.request.user

		# Limpia campos residuales del modo no activo para evitar validaciones cruzadas.
		if self.request.method == 'POST':
			data = self.request.POST.copy()
			modo = data.get('modo_usuario', CuentaComercioCreateForm.MODO_EXISTENTE)
			if modo == CuentaComercioCreateForm.MODO_NUEVO:
				data['usuario_existente'] = ''
			else:
				for field in ['username', 'first_name', 'last_name', 'email', 'id_sucursal', 'password1', 'password2']:
					data[field] = ''
			kwargs['data'] = data
		return kwargs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'accion': 'Crear Cuenta Comercio',
			'list_view_name': 'cuenta_comercio_list',
			'fecha': timezone.now(),
			'create_mode': True,
		})
		return context

	def form_valid(self, form):
		try:
			with transaction.atomic():
				modo_usuario = form.cleaned_data.get('modo_usuario')
				if modo_usuario == CuentaComercioCreateForm.MODO_NUEVO:
					user = User(
						username=form.cleaned_data.get('username').strip(),
						first_name=(form.cleaned_data.get('first_name') or '').strip(),
						last_name=(form.cleaned_data.get('last_name') or '').strip(),
						email=form.cleaned_data.get('email').strip(),
						id_sucursal=form.cleaned_data.get('id_sucursal'),
						is_active=True,
						is_staff=False,
					)
					user.set_password(form.cleaned_data.get('password1'))
					user.save()
				else:
					user = form.cleaned_data.get('usuario_existente_obj')

				_asignar_grupo_comercio(user)

				self.object = CuentaComercio.objects.create(
					user=user,
					comercio=form.cleaned_data.get('comercio'),
					activo=form.cleaned_data.get('activo'),
				)
		except IntegrityError:
			form.add_error(None, 'No se pudo guardar la vinculacion. Verifique que el usuario no este vinculado.')
			return self.form_invalid(form)

		messages.success(self.request, 'Cuenta Comercio creada correctamente.')
		return redirect(self.success_url)


class CuentaComercioUpdateView(StaffRequiredMixin, UpdateView):
	model = CuentaComercio
	form_class = CuentaComercioUpdateForm
	template_name = 'maestros/cuenta_comercio_form.html'
	success_url = reverse_lazy('cuenta_comercio_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'accion': f'Editar Cuenta Comercio - {self.object.pk}',
			'list_view_name': 'cuenta_comercio_list',
			'fecha': timezone.now(),
			'create_mode': False,
		})
		return context

	def form_valid(self, form):
		try:
			with transaction.atomic():
				response = super().form_valid(form)
				_asignar_grupo_comercio(self.object.user)
		except IntegrityError:
			form.add_error('user', 'El usuario seleccionado ya esta vinculado a otro comercio.')
			return self.form_invalid(form)

		messages.success(self.request, 'Cuenta Comercio actualizada correctamente.')
		return response


class CuentaComercioDeleteView(StaffRequiredMixin, View):
	def post(self, request, pk):
		objeto = CuentaComercio.objects.filter(pk=pk).first()
		if not objeto:
			messages.error(request, 'La Cuenta Comercio no existe o ya fue eliminada.')
			return redirect('cuenta_comercio_list')

		objeto.delete()
		messages.success(request, 'Cuenta Comercio eliminada correctamente.')
		return redirect('cuenta_comercio_list')
