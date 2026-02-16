from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers import RegistroSocioSerializer
from ...maestros.models.socio_models import Socio, SolicitudAdhesion 
from  ...maestros.models.cuenta_socio_models import CuentaSocio

User = get_user_model()

class RegistroSocioView(APIView):
    authentication_classes = []
    permission_classes = []

    @transaction.atomic
    def post(self, request):
        ser = RegistroSocioSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        # 1) Socio por CUIT
        try:
            socio = Socio.objects.get(cuit=data["cuit"])
        except Socio.DoesNotExist:
            return Response(
                {"detail": "CUIT no encontrado. Acercate a la mutual para asociarte."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1.1) Socio debe estar activo
        if not socio.estatus_socio:
            return Response(
                {"detail": "Tu cuenta de socio no está activa. Comunicate con la mutual."},
                status=status.HTTP_403_FORBIDDEN
            )


        # 2) Solicitud aprobada
        solicitud = (SolicitudAdhesion.objects
                     .filter(id_socio=socio, estado_solicitud_adhesion=2)
                     .order_by("-id_solicitud_adhesion")
                     .first())
        if not solicitud:
            return Response(
                {"detail": "Tu adhesión aún no está aprobada."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 3) Validar email/movil
        email_ok = (solicitud.email_solicitud_adhesion or socio.email_socio) == data["email"]
        movil_ok = (solicitud.movil_solicitud_adhesion or socio.movil_socio) == data["movil"]
        if not (email_ok and movil_ok):
            return Response(
                {"detail": "Email o móvil no coinciden con los datos aprobados."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4) Ya vinculado?
        if CuentaSocio.objects.filter(socio=socio).exists():
            return Response(
                {"detail": "Este socio ya tiene una cuenta creada."},
                status=status.HTTP_409_CONFLICT
            )

        # 5) Username único
        if User.objects.filter(username=data["username"]).exists():
            return Response(
                {"detail": "El nombre de usuario ya existe."},
                status=status.HTTP_409_CONFLICT
            )

        # 6) Crear usuario
        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            is_active=True,
            id_sucursal_id=1,
        )

        # 7) Grupo Usuario
        grupo, _ = Group.objects.get_or_create(name="Usuario")
        user.groups.add(grupo)

        # 8) Vincular 1 a 1
        CuentaSocio.objects.create(socio=socio, user=user, activo=True)


        refresh = RefreshToken.for_user(user)

        return Response({
            "detail": "Cuenta creada correctamente",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "id_sucursal_id": user.id_sucursal_id,
            },
            "socio": {
                "id": socio.id_socio,
                "cuit": socio.cuit,
            }
        }, status=status.HTTP_201_CREATED)


class CurrentUserView(APIView):
    """
    Endpoint que devuelve los datos del usuario actual autenticado
    con información adicional del socio asociado.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Response base con datos del usuario
        response_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "telefono": user.telefono or "",
        }
        
        # Intentar obtener la cuenta socio asociada
        try:
            cuenta_socio = user.cuenta_socio
            socio = cuenta_socio.socio
            response_data.update({
                "id_socio": socio.id_socio,
                "cuit": socio.cuit,
                "legajo": socio.legajo,
                "telefono": socio.movil_socio or user.telefono or "",
            })
        except Exception as e:
            # Si no hay cuenta socio, retornar solo datos del usuario
            pass
        
        return Response(response_data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
    Endpoint para cambiar la contraseña del usuario autenticado.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        # Obtener datos de la solicitud
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        
        # Validaciones
        if not old_password:
            return Response(
                {"detail": "La contraseña actual es requerida."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not new_password:
            return Response(
                {"detail": "La nueva contraseña es requerida."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_password != new_password_confirm:
            return Response(
                {"detail": "Las contraseñas no coinciden."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(new_password) < 6:
            return Response(
                {"detail": "La contraseña debe tener al menos 6 caracteres."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar contraseña actual
        if not user.check_password(old_password):
            return Response(
                {"detail": "La contraseña actual es incorrecta."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Cambiar contraseña
        user.set_password(new_password)
        user.save()
        
        return Response({
            "detail": "Contraseña cambiada correctamente."
        }, status=status.HTTP_200_OK)

