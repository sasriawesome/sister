from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from sister.admin.admin import ModelAdmin
from sister.admin.sites import tenant_admin


from .models import *

@admin.register(get_user_model())
class UserAdmin(UserAdminBase):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')


tenant_admin.register(get_user_model(), UserAdmin)