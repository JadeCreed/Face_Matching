"""
WSGI config for facecapstone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# Add your project folder to the Python path
path = '/home/Tripixcreed07/Face_Matching'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module (use your actual project folder name)
os.environ['DJANGO_SETTINGS_MODULE'] = 'facecapstone.settings'

# Import and set up Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
