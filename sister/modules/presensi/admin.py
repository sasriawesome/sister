from django.contrib import admin
from django.contrib.admin import ModelAdmin
from sister.contrib.admin import admin_site

from .models import (
    PresensiKelas,
    PresensiSiswa,
)


class PresensiSiswa(admin.TabularInline):
    extra = 0
    model = PresensiSiswa


class PresensiKelasAdmin(ModelAdmin):
    list_filter = ['kelas']
    inlines = [PresensiSiswa]

    def get_inlines(self, request, obj):
        if obj:
            return self.inlines
        return []


admin_site.register(PresensiKelas, PresensiKelasAdmin)
