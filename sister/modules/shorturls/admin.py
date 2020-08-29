from django.contrib.admin import ModelAdmin
from django.utils.html import format_html

from sister.core.admin import admin_site

from .models import ShortUrl


class ShortUrlAdmin(ModelAdmin):
    menu_icon = 'link'
    list_display = ['name', 'hashed_url', 'clicked', 'view_url']

    def view_url(self, obj):
        return format_html(
            "<a href='%s' target='_blank'>View</a>" % obj.get_absolute_url())


admin_site.register(ShortUrl, ShortUrlAdmin)
