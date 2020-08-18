# Application definition
# =============================================================================

INSTALLED_APPS = (

    # app where tenant model resides in
    'sister.auth',
    'sister.admin',
    'sister.api',
    'sister_web',

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
