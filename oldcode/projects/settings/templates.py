import os
from .base import PROJECT_DIR

TEMPUS_DOMINUS_LOCALIZE = False
TEMPUS_DOMINUS_INCLUDE_ASSETS = False

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
