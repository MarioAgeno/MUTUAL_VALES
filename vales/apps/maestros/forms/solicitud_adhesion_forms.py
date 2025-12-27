# vales\apps\maestros\forms\solicitud_adhesion_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.socio_models import SolicitudAdhesion
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect)


class SolicitudAdhesionForm(CrudGenericForm):
		
	class Meta:
		model = SolicitudAdhesion
		fields ='__all__'
		
		widgets = {
			'estatus_solicitud_adhesion': 
				forms.Select(attrs={**formclassselect}),
			'id_socio': 
				forms.Select(attrs={**formclassselect}),
			'cuit_solicitud_adhesion': 
				forms.TextInput(attrs={**formclasstext}),
			'movil_solicitud_adhesion': 
				forms.TextInput(attrs={**formclasstext}),
			'email_solicitud_adhesion': 
				forms.TextInput(attrs={**formclasstext}),
			'estado_solicitud_adhesion': 
				forms.Select(attrs={**formclassselect}),
		}
	
