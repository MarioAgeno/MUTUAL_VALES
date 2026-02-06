"""
WSGI config for vales project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import locale

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vales.settings')

# Fuerza punto decimal en conversiones numéricas (evita bug/edge con DECIMAL y locale)
try:
    locale.setlocale(locale.LC_NUMERIC, "C")
except locale.Error:
    pass

application = get_wsgi_application()
