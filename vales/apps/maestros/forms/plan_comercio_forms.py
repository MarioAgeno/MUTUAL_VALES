# vales\apps\maestros\forms\plan_comercio_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.comercio_models import PlanComercio
from diseno_base.diseno_bootstrap import(formclassselect)


class PlanComercioForm(CrudGenericForm):
	
	class Meta:
		model = PlanComercio
		fields ='__all__'
		
		widgets = {
			'estatus_plan_comercio':
				forms.Select(attrs={**formclassselect}),
			'id_plan':
				forms.Select(attrs={**formclassselect}),
			'id_comercio':
				forms.Select(attrs={**formclassselect}),
		}
	

		
