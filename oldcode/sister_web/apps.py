from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'sister_web'

    def ready(self):
        from sister_web import hooks, views
        hooks
        views
