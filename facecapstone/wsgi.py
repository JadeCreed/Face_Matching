import os
import sys

# Add project folder to Python path
project_home = '/home/Jade07/Face_Matching'
if project_home not in sys.path:
    sys.path.append(project_home)

# Set settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'facecapstone.settings'

# Initialize WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
