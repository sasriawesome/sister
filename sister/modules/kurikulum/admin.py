from django.contrib import admin
from sister.admin.sites import tenant_admin
from sister.admin.admin import ModelAdmin

from .models import (
    TahunAjaran,
    Kurikulum,
    MataPelajaran,
    KompetensiDasar,
    KurikulumMataPelajaran,
    Tema
)


class TahunAjaranAdmin(ModelAdmin):
    pass


class EkstraKurikulerAdmin(ModelAdmin):
    pass


class KurikulumMapelInline(admin.TabularInline):
    extra = 0
    model = KurikulumMataPelajaran


class KurikulumAdmin(ModelAdmin):
    inlines = [KurikulumMapelInline]


class MataPelajaranAdmin(ModelAdmin):
    list_display = ['kode', 'nama']


class KompetensiIntiAdmin(ModelAdmin):
    pass


class KompetensiAdmin(ModelAdmin):
    pass


class TemaAdmin(ModelAdmin):
    pass


tenant_admin.register(TahunAjaran, TahunAjaranAdmin)
tenant_admin.register(Kurikulum, KurikulumAdmin)
tenant_admin.register(MataPelajaran, MataPelajaranAdmin)
tenant_admin.register(KompetensiDasar, KompetensiAdmin)
tenant_admin.register(Tema, TemaAdmin)
