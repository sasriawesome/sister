from functools import update_wrapper
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import AdminSite
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

site_title = getattr(settings, 'PROJECT_TITLE', 'Sister')
site_sub_title = getattr(settings, 'PROJECT_SUBTITLE', 'Sistem Informasi Pelayanan Laboratorium')
site_description = getattr(settings, 'PROJECT_DESCRIPTION', 'Sistem Informasi Sekolah Terpadu')

from .views import AdminBaseView

class CustomAdminSite(AdminSite):
    """ 
        Custom Admin Site provide custom behaviour and Authentication
    """
    site_title = site_title
    site_header = site_title
    index_title = _('Site administration')

    site_url = '/'
    
    def __init__(self, name='admin'):
        super().__init__(name=name)
        self._view_registry = {}

    def each_context(self, request):
        context = super().each_context(request)
        context['site_sub_title'] = site_sub_title
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
        if issubclass(view_class_or_iterable, AdminBaseView):
            view_class_or_iterable = [view_class_or_iterable]

        for view in view_class_or_iterable:
            if not issubclass(view, AdminBaseView):
                raise ImproperlyConfigured(
                'The view class %s should be subclass of sister.admin.views.AdminBaseView' % view_class.__name__)
            
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
                    self.admin_view(view.as_view(admin_site=self), view.cacheable), 
                    name=view.url_name)
            ]
        return urls

custom_admin = CustomAdminSite(name='admin')
tenant_admin = CustomAdminSite(name='admin')