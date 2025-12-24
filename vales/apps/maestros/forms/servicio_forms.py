# vales\apps\maestros\forms\servicio_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import Servicio
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect)


class ServicioForm(CrudGenericForm):
	class Meta:
		model = Servicio
		fields = '__all__'

		widgets = {
			'estatus_servicio': 
				forms.Select(attrs={**formclassselect}), 
			'descripcion_servicio': 
				forms.TextInput(attrs={**formclasstext}),
			'importe_servicio': 
				forms.TextInput(attrs={**formclasstext}),
			'gasto_fijo_servicio': 
				forms.NumberInput(attrs={**formclasstext,
						   'min': 0, 'max': 99.99}),
			'gasto_porcentaje_servicio': 
				forms.NumberInput(attrs={**formclasstext,
						   'min': 0, 'max': 99.99}),
			'numero_servicio': 
				forms.NumberInput(attrs={**formclasstext,
						   'min': 0, 'max': 99.99}),
			'cuota_servicio': 
				forms.NumberInput(attrs={**formclasstext}),
			'plan_servicio': 
				forms.NumberInput(attrs={**formclasstext,
						   'min': 0, 'max': 99.99}),
			'posterga_vencimiento': 
				forms.NumberInput(attrs={**formclasstext,
						   'min': 0, 'max': 9}),
			'compro_servicio': 
				forms.TextInput(attrs={**formclasstext}),
		}
