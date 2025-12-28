# vales\apps\maestros\forms\solicitud_adhesion_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.socio_models import SolicitudAdhesion
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect)


class SolicitudAdhesionForm(CrudGenericForm):
    # Agregar campos adicionales para mostrar datos de Socio (no editables)
    nombre_socio = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**formclasstext, 'readonly': True})
    )
    cuit = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**formclasstext, 'readonly': True})
    )
    movil_socio = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={**formclasstext, 'readonly': True})
	)
    email_socio = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={**formclasstext, 'readonly': True})
	)

    
    class Meta:
        model = SolicitudAdhesion
        fields = '__all__'
        
        widgets = {
			'estatus_solicitud_adhesion': 
				forms.Select(attrs={**formclassselect}),
			'id_socio': 
				forms.Select(attrs={**formclassselect}),
			'cuit_solicitud_adhesion': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'movil_solicitud_adhesion': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'email_solicitud_adhesion': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'estado_solicitud_adhesion': 
				forms.Select(attrs={**formclassselect}),
		}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
		# Si hay una instancia (edición), poblar los campos adicionales con datos de Socio
        if self.instance and self.instance.pk and self.instance.id_socio:
            socio = self.instance.id_socio 
            self.fields['nombre_socio'].initial = socio.nombre_socio
            self.fields['cuit'].initial = socio.cuit
            self.fields['movil_socio'].initial = socio.movil_socio
            self.fields['email_socio'].initial = socio.email_socio
