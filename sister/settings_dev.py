"""
Django settings for Sister project.
"""
import os
import inspect
import pydf
from sister import __version__ as version

# Used by shell_plus  --notebook
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# =============================================================================
# SECURITY WARNING:
# Don't run with debug turned on in production!
# =============================================================================

DEBUG = bool(os.getenv('DEBUG', True))

# Build paths
PROJECT_NAME = 'SISTER'
PROJECT_VERSION = version
PROJECT_DESCRIPTION = """
    Django REST API boiler plate project template.
    Speed your API Developmet
"""
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SITE_ID = os.getenv('SITE_ID', int(1))

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

SECRET_KEY = os.getenv('SECRET_KEY', 'important-secret-key')

ALLOWED_HOSTS = ['*']

# =============================================================================
# Application definition
# =============================================================================

INSTALLED_APPS = (

    # app where tenant model resides in
    'sister.auth',
    'sister.admin',
    'webapp',

    # Apps dependecies

    'django_extensions',

    'widget_tweaks',
    'polymorphic',
    'import_export',
    'rest_framework',
    'drf_yasg',
    'djoser',
    'django_rq',
    'django_filters',
    'tempus_dominus',

    # The following Django contrib apps are optional
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tenant Apps
    'sister.core',
    'sister.modules.personal',
    'sister.modules.ruang',
    'sister.modules.kurikulum',
    'sister.modules.pembelajaran',
    'sister.modules.presensi',
    'sister.modules.penilaian',

    # admin app
    # 'sister.modules.adminguru',

)

WSGI_APPLICATION = 'sister.wsgi.application'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'sister.urls_tenants'
PUBLIC_SCHEMA_URLCONF = 'sister.urls_public'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sister.core.context_processors.settings',
            ],
        },
    },
]


# =============================================================================
# Database
# =============================================================================


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# If using heroku
# DATABASES['default'].update(
#    dj_database_url.config(conn_max_age=500, ssl_require=True)
# )

# =============================================================================
# Authentications
# =============================================================================

AUTH_USER_MODEL = 'sister_auth.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'rest_framework_simplejwt.authentication.JWTAuthentication'
)

ROOT_URLCONF = 'sister.urls_tenants'
PUBLIC_SCHEMA_URLCONF = 'sister.urls_public'

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

TEMPUS_DOMINUS_LOCALIZE = False
TEMPUS_DOMINUS_INCLUDE_ASSETS = False

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
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
    )

# =============================================================================
# REST FRAMEWORK
# =============================================================================

DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'sister.api.schemas.ReadWriteAutoSchema'
}

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

# =============================================================================
# Redis Cache
# =============================================================================

CACHE_TTL = 60 * 5

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # the password you should use to connect Redis is not URL-safe
            # "PASSWORD": "mysecret"
        },
        "KEY_PREFIX": os.getenv('SITE_NAME', 'sister')
    },
}

# =============================================================================
# Redis Queues
# =============================================================================

RQ_QUEUES = {
    'default': {
        'DEFAULT_TIMEOUT': 180,
        'URL': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    },
    'high': {
        'DEFAULT_TIMEOUT': 360,
        # 'PASSWORD': 'some-password',
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 1,
    },
    'low': {
        'DEFAULT_TIMEOUT': 500,
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 1,
    }
}


# =============================================================================
# Django WKHTMLTOPDF and PYDF
# =============================================================================

PYPDF_PATH = os.path.dirname(inspect.getfile(pydf))
WKHTMLTOPDF_PATH = os.path.join(PYPDF_PATH, 'bin', 'wkhtmltopdf')
WKHTMLTOPDF_CMD = os.getenv('WKHTMLTOPDF_CMD', WKHTMLTOPDF_PATH)

# Optional
# WKHTMLTOPDF_CMD_OPTIONS = {
#     'quiet': False,
# }

# If you need custom exception handlers
# RQ_EXCEPTION_HANDLERS = ['path.to.my.handler']

# =============================================================================
# Heroku Setup
# =============================================================================

# django_heroku.settings(locals())

# try:
#     from .local import *
# except ImportError:
#     pass
