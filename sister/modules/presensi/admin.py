from django.contrib import admin

from sister.admin.admin import ModelAdmin
from sister.admin.sites import tenant_admin

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


tenant_admin.register(PresensiKelas, PresensiKelasAdmin)
