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
    fields = ['siswa', 'mata_pelajaran', 'semester', 'nilai']
    readonly_fields = ['nilai']
    list_display = [
        'siswa',
        'mata_pelajaran',
        'semester',
        # 'nilai_tugas',
        # 'nilai_ph',
        # 'nilai_pts',
        # 'nilai_pas',
        'nilai',
        # 'predikat'
        'kd_list'
        ]
    inlines = [
        ItemPenilaianTugasInline,
        ItemPenilaianHarianInline,
        ItemPenilaianTengahSemesterInline,
        ItemPenilaianAkhirSemesterInline
        ]

    def get_queryset(self, request):
        return super().get_queryset(request)

    def kd_list(self, obj):
        print("KD List disini")
        print(obj.get_weighted_kd_scores())
        return 0


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
