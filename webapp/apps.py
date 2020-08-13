from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'webapp'

    def ready(self):
        import webapp.hooks
        import webapp.views
