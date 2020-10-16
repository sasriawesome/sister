from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'sister_web'

    def ready(self):
        import sister_web.views
