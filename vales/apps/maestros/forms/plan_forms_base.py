# vales \apps\maestros\forms\plan_forms.py
from django import forms
from datetime import time

from .crud_forms_generics import CrudGenericForm
from ..models.base_models import Plan
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect, formclassdate)

class PlanForm(CrudGenericForm):
	class Meta:
		model = Plan
		fields = '__all__'
		widgets = {
			'estatus_plan': forms.Select(attrs={**formclassselect}),
			'descripcion_plan': forms.TextInput(attrs={**formclasstext}),
			'cuota_plan': forms.NumberInput(attrs={**formclasstext}),
			'interes_plan': forms.NumberInput(attrs={**formclasstext,
						   'min': 0, 'max': 99.99}),
			'comision_plan': forms.NumberInput(attrs={**formclasstext,
						   'min': 0, 'max': 99.99}),
			"vigente_desde": forms.TextInput(attrs={**formclassdate, 'type': 'date'}),
			"vencimiento": forms.TextInput(attrs={**formclassdate, 'type': 'date'}),
		}
