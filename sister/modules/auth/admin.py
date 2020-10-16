from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from sister.contrib.admin import admin_site


class UserAdmin(UserAdminBase):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'),
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


admin_site.register(get_user_model(), UserAdmin)
