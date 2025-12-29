# vales\apps\maestros\forms\solicitud_vale_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.vale_models import SolcitudVale
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect, formclassdate)


class SolcitudValeForm(CrudGenericForm):
    class Meta:
        model = SolcitudVale
        fields = '__all__'
        
        widgets = {
			'estatus_solicitud_vale': 
				forms.Select(attrs={**formclassselect}),
			'id_socio': 
				forms.Select(attrs={**formclassselect}),
			'id_comercio': 
				forms.Select(attrs={**formclassselect}),
			'monto_solicitud_vale': 
				forms.NumberInput(attrs={**formclasstext}),
			'estado_solicitud_vale': 
				forms.Select(attrs={**formclassselect}),
			'limite_aprobado': 
				forms.NumberInput(attrs={**formclasstext}),
			'fecha_aprobacion': 
				forms.TextInput(attrs={'type':'date', **formclassdate, 'readonly': True}),
			'id_user': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'observaciones': 
				forms.TextInput(attrs={**formclasstext}),
		}
    
