from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from diseno_base.diseno_bootstrap import (
	formclasstext,
	formclassselect,
	formclasscheck,
)

from .crud_forms_generics import CrudGenericForm
from ..models.cuenta_comercio_models import CuentaComercio
from ..models.sucursal_models import Sucursal


User = get_user_model()


class CuentaComercioCreateForm(CrudGenericForm):
	MODO_EXISTENTE = 'existente'
	MODO_NUEVO = 'nuevo'

	MODO_USUARIO_CHOICES = [
		(MODO_EXISTENTE, 'Vincular usuario existente'),
		(MODO_NUEVO, 'Crear usuario nuevo y vincular'),
	]

	modo_usuario = forms.ChoiceField(
		label='Modo de usuario',
		choices=MODO_USUARIO_CHOICES,
		initial=MODO_EXISTENTE,
		widget=forms.RadioSelect,
	)
	usuario_existente = forms.CharField(
		label='Usuario existente',
		required=False,
		widget=forms.TextInput(attrs={**formclasstext}),
	)

	username = forms.CharField(
		label='Nombre de usuario',
		required=False,
		widget=forms.TextInput(attrs={**formclasstext}),
	)
	first_name = forms.CharField(
		label='Nombre',
		required=False,
		widget=forms.TextInput(attrs={**formclasstext}),
	)
	last_name = forms.CharField(
		label='Apellido',
		required=False,
		widget=forms.TextInput(attrs={**formclasstext}),
	)
	email = forms.EmailField(
		label='Correo electronico',
		required=False,
		widget=forms.EmailInput(attrs={**formclasstext}),
	)
	id_sucursal = forms.ModelChoiceField(
		label='Sucursal',
		queryset=Sucursal.objects.all().order_by('nombre_sucursal'),
		required=False,
		widget=forms.Select(attrs={**formclassselect}),
	)
	password1 = forms.CharField(
		label='Contrasena',
		required=False,
		widget=forms.PasswordInput(attrs={**formclasstext}),
	)
	password2 = forms.CharField(
		label='Confirmar contrasena',
		required=False,
		widget=forms.PasswordInput(attrs={**formclasstext}),
	)

	class Meta:
		model = CuentaComercio
		fields = ['comercio', 'activo']
		widgets = {
			'comercio': forms.Select(attrs={**formclassselect}),
			'activo': forms.CheckboxInput(attrs={**formclasscheck}),
		}

	def _clean_fields(self):
		"""Evita validar campos del modo no activo para prevenir errores cruzados."""
		modo = self.data.get('modo_usuario', self.MODO_EXISTENTE) if self.is_bound else self.MODO_EXISTENTE
		campos_usuario_nuevo = {'username', 'first_name', 'last_name', 'email', 'id_sucursal', 'password1', 'password2'}

		for name, bf in self._bound_items():
			if modo == self.MODO_NUEVO and name == 'usuario_existente':
				self.cleaned_data[name] = ''
				continue
			if modo == self.MODO_EXISTENTE and name in campos_usuario_nuevo:
				self.cleaned_data[name] = ''
				continue

			field = bf.field
			try:
				self.cleaned_data[name] = field._clean_bound_field(bf)
				if hasattr(self, 'clean_%s' % name):
					value = getattr(self, 'clean_%s' % name)()
					self.cleaned_data[name] = value
			except ValidationError as e:
				self.add_error(name, e)

	def __init__(self, *args, **kwargs):
		self.current_user = kwargs.pop('current_user', None)
		super().__init__(*args, **kwargs)

		self.fields['usuario_existente'].widget.attrs['placeholder'] = 'Ingrese username existente'

		if self.current_user and self.current_user.id_sucursal:
			self.fields['id_sucursal'].initial = self.current_user.id_sucursal

		# Enlaza validación al modo activo y evita errores por campos del modo oculto.
		if self.is_bound:
			self.data = self.data.copy()
			modo = self.data.get('modo_usuario', self.MODO_EXISTENTE)
			if modo == self.MODO_NUEVO:
				self.data['usuario_existente'] = ''
				self.fields['usuario_existente'].required = False
				self.fields['usuario_existente'].disabled = True
			else:
				for field in ['username', 'first_name', 'last_name', 'email', 'id_sucursal', 'password1', 'password2']:
					self.data[field] = ''
				for field in ['username', 'first_name', 'last_name', 'email', 'id_sucursal', 'password1', 'password2']:
					self.fields[field].disabled = True
				self.fields['username'].required = False
				self.fields['email'].required = False
				self.fields['password1'].required = False
				self.fields['password2'].required = False

	def clean(self):
		cleaned_data = super().clean()
		modo = cleaned_data.get('modo_usuario')

		if modo == self.MODO_EXISTENTE:
			username_existente = (cleaned_data.get('usuario_existente') or '').strip()
			if not username_existente:
				self.add_error('usuario_existente', 'Debe seleccionar un usuario existente.')
			else:
				usuario_existente = User.objects.filter(
					username=username_existente,
					cuenta_comercio__isnull=True,
				).first()
				if not usuario_existente:
					self.add_error('usuario_existente', 'El usuario seleccionado no esta disponible para vinculacion.')
				else:
					cleaned_data['usuario_existente_obj'] = usuario_existente

		if modo == self.MODO_NUEVO:
			required_fields = [
				('username', 'Debe ingresar un nombre de usuario.'),
				('email', 'Debe ingresar un correo electronico.'),
				('password1', 'Debe ingresar una contrasena.'),
				('password2', 'Debe confirmar la contrasena.'),
			]

			for field_name, error_message in required_fields:
				if not cleaned_data.get(field_name):
					self.add_error(field_name, error_message)

			username = (cleaned_data.get('username') or '').strip()
			if username and User.objects.filter(username=username).exists():
				self.add_error('username', 'El nombre de usuario ya existe.')

			email = (cleaned_data.get('email') or '').strip()
			if email and User.objects.filter(email__iexact=email).exists():
				self.add_error('email', 'Ya existe un usuario con ese correo electronico.')

			password1 = cleaned_data.get('password1')
			password2 = cleaned_data.get('password2')
			if password1 and password2 and password1 != password2:
				self.add_error('password2', 'Las contrasenas no coinciden.')

			if password1:
				try:
					validate_password(password1)
				except ValidationError as exc:
					for error in exc.messages:
						self.add_error('password1', error)

		return cleaned_data


class CuentaComercioUpdateForm(CrudGenericForm):
	class Meta:
		model = CuentaComercio
		fields = ['user', 'comercio', 'activo']
		widgets = {
			'user': forms.Select(attrs={**formclassselect}),
			'comercio': forms.Select(attrs={**formclassselect}),
			'activo': forms.CheckboxInput(attrs={**formclasscheck}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if self.instance and self.instance.pk:
			queryset = User.objects.filter(
				Q(cuenta_comercio__isnull=True) | Q(pk=self.instance.user_id)
			).order_by('username')
		else:
			queryset = User.objects.filter(cuenta_comercio__isnull=True).order_by('username')

		self.fields['user'].queryset = queryset
