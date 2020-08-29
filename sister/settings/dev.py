"""
Django settings for Sister project.
"""
import os
import inspect
import pydf
from sister import __version__ as version


# =============================================================================
# SECURITY WARNING:
# Don't run with debug turned on in production!
# =============================================================================

DEBUG = bool(os.getenv('DEBUG', True))

# Build paths

PROJECT_VERSION = version
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SITE_ID = os.getenv('SITE_ID', int(1))

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

SECRET_KEY = os.getenv('SECRET_KEY', 'important-secret-key')

ALLOWED_HOSTS = ['*']

# =============================================================================
# Application definition
# =============================================================================


SHARED_APPS = (
    'django_tenants',  # mandatory

    'tenant_users.permissions',
    'tenant_users.tenants',

    'django.contrib.contenttypes',

    # app where tenant model resides in
    'sister.tenants',
    'sister.auth',
    'sister.api',

    # Apps dependecies
    'django_cleanup.apps.CleanupConfig',
    'graphql_jwt',
    'graphene_django',
    'django_filters',

    # The following Django contrib apps are optional
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
)

TENANT_APPS = (
    # The following Django contrib apps must be in TENANT_APPS
    'tenant_users.permissions',
    'django.contrib.auth',
    'django.contrib.contenttypes',

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


TENANT_MODEL = 'sister_tenants.Sekolah'
TENANT_DOMAIN_MODEL = 'sister_tenants.Domain'

TENANT_USERS_DOMAIN = 'localhost'  # "example.com"

INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

WSGI_APPLICATION = 'sister.wsgi.application'

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'sister.urls'
PUBLIC_SCHEMA_URLCONF = 'sister.urls_public'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'sister.core.context_processors.settings',
            ],
        },
    },
]


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
        'PASSWORD': os.environ.get('PG_PASSWORD', 'habibie099'),
        'HOST': os.environ.get('PG_HOST', '127.0.0.1'),
        'PORT': os.environ.get('PG_PORT', 5432),
    }
}

# =============================================================================
# Authentications
# =============================================================================

AUTH_USER_MODEL = 'sister_auth.User'
AUTHENTICATION_BACKENDS = (
    'graphql_jwt.backends.JSONWebTokenBackend',
    'tenant_users.permissions.backend.UserBackend',
)

DJANGO_VALIDATOR = 'django.contrib.auth.password_validation.'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': DJANGO_VALIDATOR + 'UserAttributeSimilarityValidator',
    },
    {
        'NAME': DJANGO_VALIDATOR + 'MinimumLengthValidator',
    },
    {
        'NAME': DJANGO_VALIDATOR + 'CommonPasswordValidator',
    },
    {
        'NAME': DJANGO_VALIDATOR + 'NumericPasswordValidator',
    },
]


# =============================================================================
# Internationalization
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

FORMAT_MODULE_PATH = [
    'sister.formats',
]

# =============================================================================
# Static files (CSS, JavaScript, Images)
# =============================================================================

# Using AWS Bucket or Digital Ocean Space

# AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'storagename')
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'accesskeyid')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'secretaccesskey')
# AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN', 'cdn.amazonaws.com')
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_URL = '/media/'


# =============================================================================
# Email Backend
# =============================================================================

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'sister.noreply@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_USER', 'somepassword')
EMAIL_BACKEND = os.getenv(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend'
)

# =============================================================================
# GRAPHENE
# =============================================================================

GRAPHENE = {
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

# =============================================================================
# CACHES
# =============================================================================

CACHE_TTL = 60 * 5

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # the password you should use to connect Redis is not URL-safe
            # "PASSWORD": "mysecret"
        },
        "KEY_PREFIX": os.getenv('SITE_NAME', 'sister')
    },
}

# =============================================================================
# QUEUES
# =============================================================================

RQ_QUEUES = {
    'default': {
        'DEFAULT_TIMEOUT': 180,
        'URL': os.getenv('REDIS_URL', 'redis://localhost:6379/1'),
    },
    'high': {
        'DEFAULT_TIMEOUT': 360,
        # 'PASSWORD': 'some-password',
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 1,
    },
    'low': {
        'DEFAULT_TIMEOUT': 500,
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 1,
    }
}


# =============================================================================
# Django WKHTMLTOPDF and PYDF
# =============================================================================

PYPDF_PATH = os.path.dirname(inspect.getfile(pydf))
WKHTMLTOPDF_PATH = os.path.join(PYPDF_PATH, 'bin', 'wkhtmltopdf')

WKHTMLTOPDF_CMD = os.getenv('WKHTMLTOPDF_CMD', '')

# Optional
# WKHTMLTOPDF_CMD_OPTIONS = {
#     'quiet': False,
# }

# If you need custom exception handlers
# RQ_EXCEPTION_HANDLERS = ['path.to.my.handler']

TEST_RUNNER = 'snapshottest.django.TestRunner'
