from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Q


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_user_device_id_user_device_last_used_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceRelinkRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_device_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Dispositivo Anterior')),
                ('new_device_id', models.CharField(max_length=255, verbose_name='Nuevo Dispositivo')),
                ('device_model', models.CharField(blank=True, default='', max_length=255, verbose_name='Modelo de Dispositivo')),
                ('device_platform', models.CharField(blank=True, default='', max_length=50, verbose_name='Plataforma')),
                ('status', models.CharField(choices=[('PENDING', 'Pendiente'), ('APPROVED', 'Aprobada'), ('REJECTED', 'Rechazada')], default='PENDING', max_length=20, verbose_name='Estado')),
                ('requested_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Solicitud')),
                ('resolved_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Resolución')),
                ('request_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP Solicitud')),
                ('user_agent', models.TextField(blank=True, default='', verbose_name='User Agent')),
                ('resolution_notes', models.TextField(blank=True, default='', verbose_name='Notas Resolución')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_relink_requests', to='usuarios.user', verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Solicitud de Re-vinculación',
                'verbose_name_plural': 'Solicitudes de Re-vinculación',
                'ordering': ['-requested_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='devicerelinkrequest',
            constraint=models.UniqueConstraint(condition=Q(status='PENDING'), fields=('user',), name='unique_pending_device_relink_per_user'),
        ),
    ]
