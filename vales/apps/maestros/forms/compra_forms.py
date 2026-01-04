# vales\apps\maestros\forms\compra_forms.py
from django import forms
from django.core.exceptions import ValidationError
from .crud_forms_generics import CrudGenericForm
from ..models.vale_models import Compra
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect, formclassdate)


class CompraForm(CrudGenericForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Mostrar sólo socios y comercios activos en los selects
		if 'id_socio' in self.fields:
			self.fields['id_socio'].queryset = Compra._meta.get_field('id_socio').related_model.objects.filter(estatus_socio=True)
		if 'id_comercio' in self.fields:
			self.fields['id_comercio'].queryset = Compra._meta.get_field('id_comercio').related_model.objects.filter(estatus_comercio=True)

	def clean(self):
		cleaned = super().clean()
		id_socio = cleaned.get('id_socio')
		id_comercio = cleaned.get('id_comercio')
		errors = {}
		if id_socio and not getattr(id_socio, 'estatus_socio', False):
			errors['id_socio'] = 'El socio seleccionado no está activo.'
		if id_comercio and not getattr(id_comercio, 'estatus_comercio', False):
			errors['id_comercio'] = 'El comercio seleccionado no está activo.'
		if errors:
			raise ValidationError(errors)
		return cleaned

	class Meta:
		model = Compra
		fields = '__all__'

		widgets = {
			'estatus_compra':
				forms.Select(attrs={**formclassselect}),
			'id_socio':
				forms.Select(attrs={**formclassselect}),
			'id_comercio':
				forms.Select(attrs={**formclassselect}),
			'id_plan':
				forms.Select(attrs={**formclassselect}),
			'monto_compra':
				forms.NumberInput(attrs={**formclasstext}),
			'estado_compra':
				forms.Select(attrs={**formclassselect}),
			'monto_compra':
				forms.NumberInput(attrs={**formclasstext}),
			'fecha_compra':
				forms.TextInput(attrs={'type':'date', **formclassdate, 'readonly': True}),
			'autorizacion_compra':
				forms.NumberInput(attrs={**formclasstext}),
		}
    
