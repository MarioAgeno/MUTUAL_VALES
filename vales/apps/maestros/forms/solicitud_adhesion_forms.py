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
    legajo = forms.CharField(
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
			'nombre_solicitud_adhesion': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'cuit_solicitud_adhesion': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'legajo_solicitud_adhesion': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'movil_solicitud_adhesion': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'email_solicitud_adhesion': 
				forms.EmailInput(attrs={**formclasstext, 'readonly': True}),
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
            self.fields['legajo'].initial = socio.legajo
            self.fields['movil_socio'].initial = socio.movil_socio
            self.fields['email_socio'].initial = socio.email_socio

            self.fields['id_socio'].initial = self.initial.get('id_socio')
			#-- Deshabilita el campo.
            self.fields['id_socio'].widget.attrs['disabled'] = True
            self.fields['id_socio'].required = False
            self.initial['id_socio'] = self.instance.id_socio

    def clean(self):
        cleaned_data = super().clean()
        #-- Asignar automáticamente id_socio si el formulario está en modo edición.
        if self.instance.pk:
            cleaned_data['id_socio'] = self.instance.id_socio
			#-- Remover id_socio de la validación en modo edición.
            self._errors.pop('id_socio', None)
        return cleaned_data