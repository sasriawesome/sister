"""
ASGI config for Simpellab project.

"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sister_app.settings.production')

application = get_asgi_application()
