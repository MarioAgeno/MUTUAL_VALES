# \apps\maestros\urls.py
from django.urls import path

#-- Tablas
from .views.servicio_views import *
from .views.provincia_views import *
from .views.localidad_views import *
from .views.tipo_documento_identidad_views import *
from .views.tipo_iva_views import *
from .views.plan_views import *

#-- Catálogos
from .views.socio_views import *
from .views.comercio_views import *
from .views.empresa_views import *
from .views.sucursal_views import *
from .views.parametro_views import *
from .views.plan_comercio_views import *
from .views.solicitud_adhesion_views import *
from .views.solicitud_vale_views import *
from .views.compra_views import *

#-- Otras rutas.
from .views.consulta_views_maestros import filtrar_localidad
from .views.consulta_views_maestros import verificar_codigo_postal
from utils.validator.validaciones import buscar_cuit_view, buscar_cliente_id_view

urlpatterns = [
	#-- Tablas:
	#-- Servicio.
	path('servicio/', ServicioListView.as_view(), name='servicio_list'),
	path('servicio/nueva/', ServicioCreateView.as_view(), name='servicio_create'),
	path('servicio/<int:pk>/editar/', ServicioUpdateView.as_view(), name='servicio_update'),
	path('servicio/<int:pk>/eliminar/', ServicioDeleteView.as_view(), name='servicio_delete'),
	
	#-- Provincia.
	path('provincia/', ProvinciaListView.as_view(), name='provincia_list'),
	path('provincia/nueva/', ProvinciaCreateView.as_view(), name='provincia_create'),
	path('provincia/<int:pk>/editar/', ProvinciaUpdateView.as_view(), name='provincia_update'),
	path('provincia/<int:pk>/eliminar/', ProvinciaDeleteView.as_view(), name='provincia_delete'),
	
	#-- Localidad.
	path('localidad/', LocalidadListView.as_view(), name='localidad_list'),
	path('localidad/nueva/', LocalidadCreateView.as_view(), name='localidad_create'),
	path('localidad/<int:pk>/editar/', LocalidadUpdateView.as_view(), name='localidad_update'),
	path('localidad/<int:pk>/eliminar/', LocalidadDeleteView.as_view(), name='localidad_delete'),
	
	#-- TipoDocumentoIdentidad.
	path('tipo_documento_identidad/', TipoDocumentoIdentidadListView.as_view(), name='tipo_documento_identidad_list'),
	path('tipo_documento_identidad/nueva/', TipoDocumentoIdentidadCreateView.as_view(), name='tipo_documento_identidad_create'),
	path('tipo_documento_identidad/<int:pk>/editar/', TipoDocumentoIdentidadUpdateView.as_view(), name='tipo_documento_identidad_update'),
	path('tipo_documento_identidad/<int:pk>/eliminar/', TipoDocumentoIdentidadDeleteView.as_view(), name='tipo_documento_identidad_delete'),
	
	#-- TipoIva.
	path('tipo_iva/', TipoIvaListView.as_view(), name='tipo_iva_list'),
	path('tipo_iva/nueva/', TipoIvaCreateView.as_view(), name='tipo_iva_create'),
	path('tipo_iva/<int:pk>/editar/', TipoIvaUpdateView.as_view(), name='tipo_iva_update'),
	path('tipo_iva/<int:pk>/eliminar/', TipoIvaDeleteView.as_view(), name='tipo_iva_delete'),
	
	#-- Plan.
	path('plan/', PlanListView.as_view(), name='plan_list'),
	path('plan/nueva/', PlanCreateView.as_view(), name='plan_create'),
	path('plan/<int:pk>/editar/', PlanUpdateView.as_view(), name='plan_update'),
	path('plan/<int:pk>/asignar-todos/', PlanAsignarATodosView.as_view(), name='plan_asignar_todos'),
	path('plan/<int:pk>/eliminar/', PlanDeleteView.as_view(), name='plan_delete'),
    
	
	#-- Catálogos:
	#-- Socio.
	path('socio/', SocioListView.as_view(), name='socio_list'),
	path('socio/nueva/', SocioCreateView.as_view(), name='socio_create'),
	path('socio/<int:pk>/editar/', SocioUpdateView.as_view(), name='socio_update'),
	path('socio/<int:pk>/eliminar/', SocioDeleteView.as_view(), name='socio_delete'),
	
	#-- Comercio.
	path('comercio/', ComercioListView.as_view(), name='comercio_list'),
	path('comercio/nueva/', ComercioCreateView.as_view(), name='comercio_create'),
	path('comercio/<int:pk>/editar/', ComercioUpdateView.as_view(), name='comercio_update'),
	path('comercio/<int:pk>/eliminar/', ComercioDeleteView.as_view(), name='comercio_delete'),

	#-- Plan Comercio.
	path('plan_comercio/', PlanComercioListView.as_view(), name='plan_comercio_list'),
	path('plan_comercio/nueva/', PlanComercioCreateView.as_view(), name='plan_comercio_create'),
	path('plan_comercio/<int:pk>/editar/', PlanComercioUpdateView.as_view(), name='plan_comercio_update'),
	path('plan_comercio/<int:pk>/eliminar/', PlanComercioDeleteView.as_view(), name='plan_comercio_delete'),

	#-- Soclicitud Adhesion.
	path('solicitud_adhesion/', SolicitudAdhesionListView.as_view(), name='solicitud_adhesion_list'),
	path('solicitud_adhesion/nueva/', SolicitudAdhesionCreateView.as_view(), name='solicitud_adhesion_create'),
	path('solicitud_adhesion/<int:pk>/editar/', SolicitudAdhesionUpdateView.as_view(), name='solicitud_adhesion_update'),
	path('solicitud_adhesion/<int:pk>/eliminar/', SolicitudAdhesionDeleteView.as_view(), name='solicitud_adhesion_delete'),

	#-- Empresa.
	path('empresa/', EmpresaListView.as_view(), name='empresa_list'),
	path('empresa/nueva/', EmpresaCreateView.as_view(), name='empresa_create'),
	path('empresa/<int:pk>/editar/', EmpresaUpdateView.as_view(), name='empresa_update'),
	path('empresa/<int:pk>/eliminar/', EmpresaDeleteView.as_view(), name='empresa_delete'),
	
	#-- Sucursal.
	path('sucursal/', SucursalListView.as_view(), name='sucursal_list'),
	path('sucursal/nueva/', SucursalCreateView.as_view(), name='sucursal_create'),
	path('sucursal/<int:pk>/editar/', SucursalUpdateView.as_view(), name='sucursal_update'),
	path('sucursal/<int:pk>/eliminar/', SucursalDeleteView.as_view(), name='sucursal_delete'),
	
	#-- Parametro.
	path('parametro/', ParametroListView.as_view(), name='parametro_list'),
	path('parametro/nueva/', ParametroCreateView.as_view(), name='parametro_create'),
	path('parametro/<int:pk>/editar/', ParametroUpdateView.as_view(), name='parametro_update'),
	path('parametro/<int:pk>/eliminar/', ParametroDeleteView.as_view(), name='parametro_delete'),

	#-- Soclicitud Vales.
	path('solicitud_vale/', SolicitudValeListView.as_view(), name='solicitud_vale_list'),
	path('solicitud_vale/nueva/', SolicitudValeCreateView.as_view(), name='solicitud_vale_create'),
	path('solicitud_vale/<int:pk>/editar/', SolicitudValeUpdateView.as_view(), name='solicitud_vale_update'),
	path('solicitud_vale/<int:pk>/eliminar/', SolicitudValeDeleteView.as_view(), name='solicitud_vale_delete'),

	#-- Compras.
	path('compra/', CompraListView.as_view(), name='compra_list'),
	path('compra/nueva/', CompraCreateView.as_view(), name='compra_create'),
	path('compra/<int:pk>/editar/', CompraUpdateView.as_view(), name='compra_update'),
	path('compra/<int:pk>/eliminar/', CompraDeleteView.as_view(), name='compra_delete'),

	#-- Otras rutas.
	path('filtrar-localidad/', filtrar_localidad, name='filtrar_localidad'),
	path('verificar-codigo-postal/', verificar_codigo_postal, name='verificar_codigo_postal'),
	path('buscar-cuit/', buscar_cuit_view, name='buscar_cuit'),
	path('buscar-cliente-id/', buscar_cliente_id_view, name='buscar_cliente_id'),
]