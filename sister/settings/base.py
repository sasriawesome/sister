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

PROJECT_VERSION = version

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

SITE_ID = os.getenv('SITE_ID', int(1))

WSGI_APPLICATION = 'sister.wsgi.application'

ROOT_URLCONF = 'sister.urls'

PUBLIC_SCHEMA_URLCONF = 'sister.urls_public'

BASE_APPS = (

    # app where tenant model resides in
    'sister.auth',
    'sister.api',

    # Apps dependecies
    'django_cleanup.apps.CleanupConfig',
    'graphene_django',
    'django_filters',

    # The following Django contrib apps are optional
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Tenant Apps
    'sister.core',
    'sister.modules.personal',
    'sister.modules.ruang',
    'sister.modules.kurikulum',
    'sister.modules.pembelajaran',
    'sister.modules.presensi',
    'sister.modules.penilaian',
    'sister.modules.ekskul',
)

# =============================================================================
# Database
# =============================================================================

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.environ.get('PG_DATABASE', 'sister_db'),
        'USER': os.environ.get('PG_USER', 'postgres'),
        'PASSWORD': os.environ.get('PG_PASSWORD', 'sister_password'),
        'HOST': os.environ.get('PG_HOST', '127.0.0.1'),
        'PORT': os.environ.get('PG_', 5432),
    }
}