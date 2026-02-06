"""
ASGI config for vales project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
import locale

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vales.settings')

try:
    locale.setlocale(locale.LC_NUMERIC, "C")
except locale.Error:
    pass

application = get_asgi_application()
