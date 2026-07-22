"""
WSGI config for 2doList project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '2doList.settings')

application = get_wsgi_application()
