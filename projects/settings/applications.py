# Application definition
# =============================================================================

INSTALLED_APPS = (

    # app where tenant model resides in
    # 'sister.admin',
    # 'sister_web',
    'sister.auth',
    'sister.api',

    # Apps dependecies

    'django_extensions',

    'django_cleanup.apps.CleanupConfig',
    'graphene_django',
    'django_filters',
    # 'django_rq',
    # 'polymorphic',
    # 'import_export',
    # 'widget_tweaks',
    # 'tempus_dominus',

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
    'sister.modules.ekskul',

    # admin app
    # 'sister.modules.adminguru',
    # 'sister.api',
    # 'rest_framework',
    # 'drf_yasg',
    # 'djoser',
)
