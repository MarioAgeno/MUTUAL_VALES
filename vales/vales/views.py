# vales\vales\views.py
from django.shortcuts import render, redirect
from django.utils import timezone


def home_view(request):
	if request.user.is_authenticated:
		es_comercio = (
			not request.user.is_superuser
			and not request.user.is_staff
			and request.user.groups.filter(name='Comercio').exists()
		)
		if es_comercio:
			return redirect('compra_list')

		fecha_actual = timezone.now()
		return render(request, 'home.html', {'fecha': fecha_actual})
	else:
		return redirect('iniciar_sesion')