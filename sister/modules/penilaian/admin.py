from django.contrib import admin
from django.contrib.admin import ModelAdmin

from sister.core.admin import admin_site

from .models import (
    PenilaianPembelajaran,
    ItemPenilaian
)


class ItemPenilaianInline(admin.TabularInline):
    extra = 0
    model = ItemPenilaian


class PenilaianPembelajaranAdmin(ModelAdmin):
    list_display = [
        'siswa',
        'mata_pelajaran',
        'semester',
        # 'nilai_tugas',
        # 'nilai_ph',
        # 'nilai_pts',
        # 'nilai_pas',
        # 'nilai',
        # 'predikat'
    ]
    inlines = [
        ItemPenilaianInline
    ]

    def get_queryset(self, request):
        return super().get_queryset(request)


admin_site.register(PenilaianPembelajaran, PenilaianPembelajaranAdmin)
