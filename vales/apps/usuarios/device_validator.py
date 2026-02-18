"""
Utilidades para validación de dispositivos en Django
"""
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied


def validar_dispositivo_usuario(user, request, strict=True):
    """
    Valida que el dispositivo usado coincida con el registrado del usuario.
    
    Args:
        user: Instancia del usuario de Django
        request: Request object de DRF
        strict: Si True, rechaza si no coincide. Si False, solo advierte.
    
    Raises:
        PermissionDenied: Si el dispositivo no está autorizado (strict=True)
    """
    # Extraer información del dispositivo del request
    device_id = (
        request.data.get("device_id") or 
        request.META.get("HTTP_X_DEVICE_ID")
    )
    device_model = (
        request.data.get("device_model") or 
        request.META.get("HTTP_X_DEVICE_MODEL")
    )
    device_platform = (
        request.data.get("device_platform") or 
        request.META.get("HTTP_X_DEVICE_PLATFORM")
    )
    
    # 🔍 LOG TEMPORAL para debugging
    print(f"🔍 VALIDACIÓN DISPOSITIVO:")
    print(f"   Usuario: {user.username}")
    print(f"   Device recibido: {device_id}")
    print(f"   Device en BD: {user.device_id}")
    print(f"   Modelo recibido: {device_model}")
    print(f"   Strict mode: {strict}")
    
    # Si no hay device_id, permitir por retrocompatibilidad
    if not device_id:
        print(f"   ⚠️ No se recibió device_id - PERMITIENDO por retrocompatibilidad")
        return
    
    # Si el usuario no tiene device_id registrado, es primera vez - actualizar
    if not user.device_id:
        print(f"   ✅ Primera vez - REGISTRANDO device_id")
        user.device_id = device_id
        user.device_model = device_model
        user.device_platform = device_platform
        user.device_registered_at = timezone.now()
        user.device_last_used_at = timezone.now()
        user.save()
        return
    
    # Validar que el device_id coincida
    if device_id != user.device_id:
        print(f"   ❌ Device NO coincide - {'BLOQUEANDO' if strict else 'PERMITIENDO (no strict)'}")
        if strict:
            raise PermissionDenied(
                "Dispositivo no autorizado. Esta operación solo puede realizarse "
                "desde el dispositivo registrado."
            )
        else:
            # Solo advertir pero permitir (para casos especiales)
            pass
    else:
        print(f"   ✅ Device coincide - PERMITIENDO")
    
    # Si coincide, actualizar última vez usado
    user.device_last_used_at = timezone.now()
    user.save()


def actualizar_dispositivo_usuario(user, device_id, device_model=None, device_platform=None):
    """
    Actualiza la información del dispositivo del usuario sin validar.
    Útil para actualizaciones forzadas o primer registro.
    """
    if device_id:
        user.device_id = device_id
        user.device_model = device_model
        user.device_platform = device_platform
        if not user.device_registered_at:
            user.device_registered_at = timezone.now()
        user.device_last_used_at = timezone.now()
        user.save()
