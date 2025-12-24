# vales\apps\maestros\forms\parametro_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import Parametro
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect, formclassdate)

class ParametroForm(CrudGenericForm):
	
	class Meta:
		model = Parametro
		fields = '__all__'
		
		widgets = {
			'estatus_parametro':
				forms.Select(attrs={**formclassselect}),
			'id_empresa':
				forms.Select(attrs={**formclassselect}),
			'interes':
				forms.NumberInput(attrs={**formclasstext,
						   'min': 0, 'max': 99.99}),
			'fecha_vencimiento': 
				forms.TextInput(attrs={'type':'date', **formclassdate}),

		}
