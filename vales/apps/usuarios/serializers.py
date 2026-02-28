from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DeviceRelinkRequest

User = get_user_model()

class RegistroSocioSerializer(serializers.Serializer):
    cuit = serializers.IntegerField()
    email = serializers.EmailField()
    movil = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    
    # Campos de dispositivo (opcionales para retrocompatibilidad)
    device_id = serializers.CharField(max_length=255, required=False, allow_null=True)
    device_model = serializers.CharField(max_length=255, required=False, allow_null=True)
    device_platform = serializers.CharField(max_length=50, required=False, allow_null=True)


class DeviceRelinkRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    device_id = serializers.CharField(max_length=255)
    device_model = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    device_platform = serializers.CharField(max_length=50, required=False, allow_blank=True, default='')

    def validate(self, attrs):
        username = attrs['username'].strip()
        password = attrs['password']
        new_device_id = attrs['device_id'].strip()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'Credenciales inválidas.'})

        if not user.check_password(password):
            raise serializers.ValidationError({'detail': 'Credenciales inválidas.'})

        if not user.is_active:
            raise serializers.ValidationError({'detail': 'Usuario inactivo.'})

        if not new_device_id:
            raise serializers.ValidationError({'detail': 'device_id es requerido.'})

        if user.device_id and user.device_id == new_device_id:
            raise serializers.ValidationError({'detail': 'El dispositivo ya está vinculado a este usuario.'})

        has_pending = DeviceRelinkRequest.objects.filter(
            user=user,
            status=DeviceRelinkRequest.STATUS_PENDING,
        ).exists()

        if has_pending:
            raise serializers.ValidationError({'detail': 'Ya existe una solicitud pendiente para este usuario.'})

        attrs['user_obj'] = user
        attrs['new_device_id'] = new_device_id
        attrs['old_device_id'] = user.device_id
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')

        return DeviceRelinkRequest.objects.create(
            user=validated_data['user_obj'],
            old_device_id=validated_data.get('old_device_id'),
            new_device_id=validated_data['new_device_id'],
            device_model=validated_data.get('device_model', ''),
            device_platform=validated_data.get('device_platform', ''),
            request_ip=request.META.get('REMOTE_ADDR') if request else None,
            user_agent=request.META.get('HTTP_USER_AGENT', '') if request else '',
        )
