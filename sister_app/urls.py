"""
Sister Tenant URL Configuration

"""
from django.conf import settings
from django.urls import path, include

from sister.contrib.admin import admin_site
from sister_web.sites import website

urlpatterns = [
    path('', include(website.get_urls())),
    # path('api/', include('sister.api.urls_tenant')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += [
        path('admin/', include((admin_site.get_urls(), 'admin'))),
    ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )


urlpatterns = urlpatterns + []
