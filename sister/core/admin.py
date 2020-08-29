from django.contrib.admin import AdminSite
from django.core.exceptions import ImproperlyConfigured


class AdminViewMixin:
    pass


class CustomAdminSite(AdminSite):
    """
        Custom Admin Site provide custom behaviour and Authentication
    """

    site_url = '/'

    def __init__(self, name='admin'):
        super().__init__(name=name)
        self._view_registry = {}

    def each_context(self, request):
        context = super().each_context(request)
        return context

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_staff

    def register_view(self, view_class_or_iterable=None, **options):
        """
        Register the given view class.
        The view class(s) subclass of sister AdminBaseView.
        """
        if issubclass(view_class_or_iterable, AdminViewMixin):
            view_class_or_iterable = [view_class_or_iterable]

        for view in view_class_or_iterable:
            if not issubclass(view, AdminViewMixin):
                raise ImproperlyConfigured(
                    'The view class %s ' % view.__name__
                    + 'should be subclass of sister.admin.views.AdminBaseView'
                )

            self._view_registry[view] = view(self)

    def unregister_view(self, view_class):
        """ Todo Next """
        pass

    def is_view_registered(self, view):
        """ Todo Next """
        pass

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        for view, instance in self._view_registry.items():
            urls += [
                path(
                    view.url_path,
                    self.admin_view(view.as_view(
                        admin_site=self), view.cacheable),
                    name=view.url_name)
            ]
        return urls


admin_site = CustomAdminSite(name='admin')
