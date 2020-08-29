
from django.contrib.admin import ModelAdmin
from sister.core.admin import admin_site
from sister.modules.ruang.models import Ruang


class RuangAdmin(ModelAdmin):
    list_display = ['kode', 'nama', 'kapasitas']


admin_site.register(Ruang, RuangAdmin)
