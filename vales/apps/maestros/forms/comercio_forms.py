# vales\apps\maestros\forms\comercio_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import *
from ..models.comercio_models import Comercio
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect, formclasscheck)


class ComercioForm(CrudGenericForm):
	
	class Meta:
		model = Comercio
		fields = '__all__'
		
		widgets = {
			'estatus_comercio': 
				forms.Select(attrs={**formclassselect}),
			'nombre_comercio': 
				forms.TextInput(attrs={**formclasstext}),
			'domicilio_comercio': 
				forms.TextInput(attrs={**formclasstext}),
			'id_provincia': 
				forms.Select(attrs={**formclassselect}),
			'id_localidad': 
				forms.Select(attrs={**formclassselect}),
			'codigo_postal': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'id_tipo_iva': 
				forms.Select(attrs={**formclassselect}),
			'cuit': 
				forms.TextInput(attrs={**formclasstext}),
			'telefono_comercio': 
				forms.TextInput(attrs={**formclasstext}),
			'movil_comercio': 
				forms.TextInput(attrs={**formclasstext}),
			'email_comercio': 
				forms.EmailInput(attrs={**formclasstext}),
			'id_servicio': 
				forms.Select(attrs={**formclassselect}),
			'pago': 
				forms.Select(attrs={**formclassselect}),
			'bonificacion_comercio':
				forms.NumberInput(attrs={**formclasstext,
						   'min': 0, 'max': 99.99}),
			'gasto_adm_comercio':
				forms.NumberInput(attrs={**formclasstext,
						   'min': 0, 'max': 99.99}),
			'observacion_comercio': 
				forms.Textarea(attrs={**formclasstext, 'rows': '3'}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.fields['id_localidad'].choices = []
		
		#-- Verificar si el formulario se llama con datos (POST).
		if self.is_bound:
			#-- Obtener el valor enviado de id_provincia_tarjeta.
			provincia_id = self.data.get('id_provincia')
			localidad_id = self.data.get('id_localidad', '')
			
			if provincia_id:
				#-- Filtrar localidades según la provincia enviada.
				localidades = Localidad.objects.filter(id_provincia=provincia_id).order_by('nombre_localidad')
				self.fields['id_localidad'].choices = [("", "Seleccione una localidad")] + [
					(loc.id_localidad, f"{loc.nombre_localidad} - {loc.codigo_postal}") for loc in localidades
				]
				self.initial['id_localidad'] = localidad_id
			else:
				self.fields['id_localidad'].choices = [("", "Seleccione una localidad")]
			
		#-- Si se está editando un registro existente.
		elif self.instance and self.instance.pk and self.instance.id_provincia:
			localidades = Localidad.objects.filter(id_provincia=self.instance.id_provincia).order_by('nombre_localidad')
			self.fields['id_localidad'].choices = [
				(loc.id_localidad, f"{loc.nombre_localidad} - {loc.codigo_postal}")
				for loc in localidades
			]
			
			#-- Establecer localidad seleccionada inicialmente.
			if self.instance.id_localidad:
				self.initial['id_localidad'] = self.instance.id_localidad.id_localidad
		
		#-- Asegurar que exista una opción inicial en cualquier caso.
		self.fields['id_localidad'].choices.insert(0, ("", "Seleccione una localidad"))