# Authentications
# =============================================================================

AUTH_USER_MODEL = 'sister_auth.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'rest_framework_simplejwt.authentication.JWTAuthentication'
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
