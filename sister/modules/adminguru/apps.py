from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'sister.modules.adminguru'

    def ready(self):
        import sister.modules.adminguru.hooks