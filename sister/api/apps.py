from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    label = 'sister_api'
    name = 'sister.api'
    verbose_name = 'Sister API GraphQl'
