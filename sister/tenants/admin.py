from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from sister.core.admin import admin_site
from sister.tenants.models import Client


class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'paid_until')


admin_site.register(Client, ClientAdmin)
