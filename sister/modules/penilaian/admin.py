from django.contrib import admin

from sister.admin.admin import ModelAdmin
from sister.admin.sites import tenant_admin

from .models import (
    PenilaianPembelajaran,
    ItemPenilaianTugas,
    ItemPenilaianHarian,
    ItemPenilaianTengahSemester,
    ItemPenilaianAkhirSemester
)


class MataPelajaranKelasAdmin(ModelAdmin):
    list_display = ['kelas', 'mata_pelajaran', 'guru']


class ItemPenilaianTugasInline(admin.TabularInline):
    extra = 0
    model = ItemPenilaianTugas


class ItemPenilaianHarianInline(admin.TabularInline):
    extra = 0
    model = ItemPenilaianHarian


class ItemPenilaianTengahSemesterInline(admin.TabularInline):
    extra = 0
    model = ItemPenilaianTengahSemester


class ItemPenilaianAkhirSemesterInline(admin.TabularInline):
    extra = 0
    model = ItemPenilaianAkhirSemester


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
        ItemPenilaianTugasInline,
        ItemPenilaianHarianInline,
        ItemPenilaianTengahSemesterInline,
        ItemPenilaianAkhirSemesterInline
        ]

    def get_queryset(self, request):
        return super().get_queryset(request)


class PenilaianEkstraKurikulerAdmin(ModelAdmin):
    fields = ['siswa', 'ekskul', 'semester', 'nilai']
    list_display = [
        'siswa',
        'ekskul',
        'semester',
        'nilai',
        # 'predikat'
        ]


tenant_admin.register(PenilaianPembelajaran, PenilaianPembelajaranAdmin)
