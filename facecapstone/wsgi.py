import os
import sys

# Add your project folder to the Python path
project_home = '/home/Jade07/Face_Matching'
if project_home not in sys.path:
    sys.path.append(project_home)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'facecapstone.settings'

# Activate virtualenv
activate_this = '/home/Jade07/Face_Matching/venv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Initialize WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
