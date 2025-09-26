"""
WSGI config for facecapstone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# Add project folder (where manage.py lives)
path = '/home/Tripixcreed07/Face_Matching'
if path not in sys.path:
    sys.path.append(path)

# Set settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'facecapstone.settings'

# Initialize application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
