"""
WSGI config for educational_process project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core import wsgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educational_process.settings')

application = wsgi.get_wsgi_application()
