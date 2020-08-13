from django.contrib import admin

from sister.admin.sites import tenant_admin
from sister.admin.admin import ModelAdmin

from .models import (
    TahunAjaran,
    Kurikulum,
    MataPelajaran,
    MataPelajaranKurikulum,
    KompetensiInti,
    KompetensiDasar,
    Tema
)


class TahunAjaranAdmin(ModelAdmin):
    pass


class EkstraKurikulerAdmin(ModelAdmin):
    pass


class MataPelajaranKurikulumInline(admin.TabularInline):
    extra = 1
    model = MataPelajaranKurikulum


class KurikulumAdmin(ModelAdmin):
    inlines = [MataPelajaranKurikulumInline]


class MataPelajaranAdmin(ModelAdmin):
    list_display = ['kode', 'nama']


class KompetensiIntiAdmin(ModelAdmin):
    pass


class KompetensiDasarAdmin(ModelAdmin):
    pass


class TemaAdmin(ModelAdmin):
    pass


tenant_admin.register(TahunAjaran, TahunAjaranAdmin)
tenant_admin.register(Kurikulum, KurikulumAdmin)
tenant_admin.register(MataPelajaran, MataPelajaranAdmin)
tenant_admin.register(KompetensiInti, KompetensiIntiAdmin)
tenant_admin.register(KompetensiDasar, KompetensiDasarAdmin)
tenant_admin.register(Tema, TemaAdmin)
