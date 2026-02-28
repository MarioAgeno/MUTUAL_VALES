from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

#from apps.usuarios.models.user_models import User
from apps.usuarios.models import User, DeviceRelinkRequest

#-- Esta configuración es para que aparezcan los nuevos campos en el Panel Adm.
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        *BaseUserAdmin.fieldsets,
        (
            'Datos Adicionales',
            {
                'fields': (
                    'email_alt',
                    'telefono',
                ),
            },
        ),
    )

admin.site.register(User, UserAdmin)


@admin.register(DeviceRelinkRequest)
class DeviceRelinkRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'old_device_id',
        'new_device_id',
        'device_platform',
        'requested_at',
        'resolved_at',
    )
    list_filter = ('status', 'device_platform', 'requested_at')
    search_fields = ('user__username', 'old_device_id', 'new_device_id', 'request_ip')
    readonly_fields = ('requested_at', 'request_ip', 'user_agent', 'old_device_id')
    actions = ['approve_requests', 'reject_requests']

    @admin.action(description='Aprobar solicitudes seleccionadas')
    def approve_requests(self, request, queryset):
        updated = 0
        for relink in queryset.filter(status=DeviceRelinkRequest.STATUS_PENDING):
            user = relink.user
            now = timezone.now()

            user.device_id = relink.new_device_id
            user.device_model = relink.device_model
            user.device_platform = relink.device_platform
            if not user.device_registered_at:
                user.device_registered_at = now
            user.device_last_used_at = now
            user.save(update_fields=[
                'device_id',
                'device_model',
                'device_platform',
                'device_registered_at',
                'device_last_used_at',
            ])

            try:
                cuenta_socio = user.cuenta_socio
                socio = cuenta_socio.socio

                socio.device_id = relink.new_device_id
                socio.device_model = relink.device_model
                socio.device_platform = relink.device_platform
                if not socio.device_registered_at:
                    socio.device_registered_at = now
                socio.device_last_used_at = now
                socio.save(update_fields=[
                    'device_id',
                    'device_model',
                    'device_platform',
                    'device_registered_at',
                    'device_last_used_at',
                ])
            except ObjectDoesNotExist:
                pass

            relink.status = DeviceRelinkRequest.STATUS_APPROVED
            relink.resolved_at = now
            relink.resolution_notes = 'Aprobada desde Django Admin.'
            relink.save(update_fields=['status', 'resolved_at', 'resolution_notes'])
            updated += 1

        self.message_user(request, f'Solicitudes aprobadas: {updated}')

    @admin.action(description='Rechazar solicitudes seleccionadas')
    def reject_requests(self, request, queryset):
        now = timezone.now()
        updated = queryset.filter(status=DeviceRelinkRequest.STATUS_PENDING).update(
            status=DeviceRelinkRequest.STATUS_REJECTED,
            resolved_at=now,
            resolution_notes='Rechazada desde Django Admin.',
        )
        self.message_user(request, f'Solicitudes rechazadas: {updated}')