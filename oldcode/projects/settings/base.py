"""
Django settings for Sister project.
"""
import os
from sister import __version__ as version

# Used by shell_plus  --notebook
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# =============================================================================
# SECURITY WARNING:
# Don't run with debug turned on in production!
# =============================================================================

DEBUG = bool(os.getenv('DEBUG', False))
SECRET_KEY = os.getenv('SECRET_KEY', 'important-secret-key')

# Build paths

PROJECT_NAME = 'SISTER'
PROJECT_VERSION = version
PROJECT_DESCRIPTION = """
    Django REST API boiler plate project template.
    Speed your API Developmet
"""
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

SITE_ID = os.getenv('SITE_ID', int(1))

WSGI_APPLICATION = 'projects.wsgi.application'

ROOT_URLCONF = 'projects.urls_tenants'

PUBLIC_SCHEMA_URLCONF = 'projects.urls_public'
