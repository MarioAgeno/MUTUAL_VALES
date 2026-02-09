from rest_framework import serializers

class RegistroSocioSerializer(serializers.Serializer):
    cuit = serializers.IntegerField()
    email = serializers.EmailField()
    movil = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
