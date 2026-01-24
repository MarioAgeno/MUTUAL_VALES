# vales\apps\maestros\forms\compra_forms.py
from django import forms
from django.core.exceptions import ValidationError
from .crud_forms_generics import CrudGenericForm
from ..models.vale_models import Compra
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect, formclassdate)


class CompraForm(CrudGenericForm):
	def __init__(self, *args, **kwargs):
		# Filtrar los valores de los campos id_solicitud_vale
		super().__init__(*args, **kwargs)
		if 'id_solicitud_vale' in self.fields:
			self.fields['id_solicitud_vale'].queryset = Compra._meta.get_field('id_solicitud_vale').related_model.objects.filter(estado_solicitud_vale=2)
		# Mostrar sólo socios y comercios activos en los selects
		if 'id_socio' in self.fields:
			self.fields['id_socio'].queryset = Compra._meta.get_field('id_socio').related_model.objects.filter(estatus_socio=True)
		if 'id_comercio' in self.fields:
			self.fields['id_comercio'].queryset = Compra._meta.get_field('id_comercio').related_model.objects.filter(estatus_comercio=True)

		# Deshabilitar campos id_socio e id_comercio al crear un nuevo registro
		if not self.instance.pk:
			for f in ["id_socio", "id_comercio"]:
				if f in self.fields:
					self.fields[f].disabled = True
					self.fields[f].required = False



	def clean(self):
		cleaned = super().clean()

		solicitud = cleaned.get("id_solicitud_vale")
		if solicitud:
			cleaned["id_socio"] = solicitud.id_socio
			cleaned["id_comercio"] = solicitud.id_comercio

			# También conviene setearlo en la instancia para asegurar guardado
			self.instance.id_socio = cleaned["id_socio"]
			self.instance.id_comercio = cleaned["id_comercio"]

		# ... tu validación actual de activos
		return cleaned

	class Meta:
		model = Compra
		fields = '__all__'

		widgets = {
			'estatus_compra':
				forms.Select(attrs={**formclassselect}),
			'id_solicitud_vale':
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
    
