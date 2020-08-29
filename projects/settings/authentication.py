# Authentications
# =============================================================================

AUTH_USER_MODEL = 'sister_auth.User'

AUTHENTICATION_BACKENDS = (
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
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
