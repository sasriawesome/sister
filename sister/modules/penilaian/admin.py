from django.contrib import admin

from sister.admin.admin import ModelAdmin
from sister.admin.sites import tenant_admin

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


tenant_admin.register(PenilaianPembelajaran, PenilaianPembelajaranAdmin)
