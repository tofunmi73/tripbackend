"""
WSGI config for spotter_trip_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spotter_trip_app.settings')

application = get_wsgi_application()

# This is for Vercel serverless function
def handler(request, **kwargs):
    return application(request, **kwargs)

app = application