# D:\MUTUAL_VALES\vales\apps\usuarios\urls.py
from django.urls import path
from apps.usuarios.views.user_views import *
from .views.api_views import RegistroSocioView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
	#-- Login/Logout
	path('sesion/iniciar/', CustomLoginView.as_view(), name='iniciar_sesion'),
	path('sesion/cerrar/', CustomLogoutView.as_view(), name='cerrar_sesion'),
	
	#-- Grupos
	path('grupo/listar/', GrupoListView.as_view(), name='grupo_listar'),
	path('grupo/crear/', GrupoCreateView.as_view(), name='grupo_crear'),
	path('grupo/editar/<int:pk>/', GrupoUpdateView.as_view(), name='grupo_editar'),
	path('grupo/eliminar/<int:pk>/', GrupoDeleteView.as_view(), name='grupo_eliminar'),
	
	#-- Usuarios
	path('usuario/listar/', UsuarioListView.as_view(), name='usuario_listar'),
	path('usuario/crear/', UsuarioCreateView.as_view(), name='usuario_crear'),
	path('usuario/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_editar'),
	path('usuario/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_eliminar'),

	# -- API
    path("registro-socio/", RegistroSocioView.as_view(), name="registro-socio"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
