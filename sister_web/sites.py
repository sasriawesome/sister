from django.core.exceptions import ImproperlyConfigured
from .options import WebViewMixin


class WebApp:

    title = 'Website'
    description = 'Awesome Website'
    index_template_name = 'sister_web/pages/index.html'

    def __init__(self, name='sister_web'):
        self.name = name
        self._registry = {}

    def register(self, view_class_or_iterable=None, **options):
        """
        Register the given view class.
        The view class(s) subclass of sister WebView.
        """
        if not isinstance(view_class_or_iterable, (list, tuple)):
            view_class_or_iterable = [view_class_or_iterable]

        for view in view_class_or_iterable:
            if view is None or view in self._registry.keys():
                continue
            if not issubclass(view, WebViewMixin):
                raise ImproperlyConfigured(
                    f'The view class {view.__name__} should be subclass'
                    + 'of sister.admin.views.AdminBaseView'
                    )
            self._registry[view] = view(self)

    def unregister(self, view_class):
        """ Todo Next """
        if view_class in self._registry.keys():
            self._registry.pop(view_class)

    def get_urls(self):
        from django.urls import path
        urls = []
        for view, instance in self._registry.items():
            urls += [
                path(
                    view.url_path,
                    view.as_view(website=self),
                    name="%s_%s" % (self.name, view.url_name))
            ]
        return urls


website = WebApp(name='sister_web')
