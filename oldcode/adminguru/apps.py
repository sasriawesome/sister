from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'sister.modules.adminguru'

    def ready(self):
        from sister.modules.adminguru import hooks
        hooks
