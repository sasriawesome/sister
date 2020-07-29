"""
Simpellab TEST URL Configuration

"""
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('api/', include('simpellab.api.urls'))
]

if settings.DEBUG:
    from django.contrib import admin
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]