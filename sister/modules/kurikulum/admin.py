from django.contrib import admin
from django.contrib.admin import ModelAdmin
from sister.core.admin import admin_site

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


admin_site.register(TahunAjaran, TahunAjaranAdmin)
admin_site.register(Kurikulum, KurikulumAdmin)
admin_site.register(MataPelajaran, MataPelajaranAdmin)
admin_site.register(KompetensiDasar, KompetensiAdmin)
admin_site.register(Tema, TemaAdmin)
