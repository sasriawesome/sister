from django.contrib import admin
from django.contrib.admin import ModelAdmin

from sister.core.admin import admin_site

from .models import (
    Kelas,
    MataPelajaranKelas,
    JadwalPelajaran,
    JadwalPiketSiswa,
    SiswaKelas,
    RentangNilai,
    KompetensiPenilaian
)


class TahunAjaranAdmin(ModelAdmin):
    pass


class KompetensiPenilaianInline(admin.TabularInline):
    extra = 0
    model = KompetensiPenilaian


class MataPelajaranKelasInline(admin.TabularInline):
    extra = 1
    model = MataPelajaranKelas


class JadwalPelajaranInline(admin.TabularInline):
    extra = 1
    model = JadwalPelajaran


class JadwalPiketSiswaInline(admin.TabularInline):
    extra = 1
    model = JadwalPiketSiswa


class SiswaKelasInline(admin.TabularInline):
    extra = 1
    model = SiswaKelas


class RentangNilaiInline(admin.TabularInline):
    extra = 0
    model = RentangNilai


class KelasAdmin(ModelAdmin):
    list_per_page = 1
    search_fields = [
        'nama_kelas',
        'guru_kelas__nip',
        'guru_kelas__person__full_name'
    ]
    list_display = [
        'nama_kelas',
        'guru_kelas',
        'tahun_ajaran'
    ]
    list_select_related = ['guru_kelas', 'tahun_ajaran']
    inlines = [
        MataPelajaranKelasInline,
        SiswaKelasInline,
    ]


class RentangNilaiAdmin(ModelAdmin):
    list_display = [
        'kelas',
        'nilai_minimum',
        'nilai_maximum',
        'predikat',
        'aksi'
    ]


class MataPelajaranKelasAdmin(ModelAdmin):
    list_display = ['kelas', 'mata_pelajaran', 'guru']
    inlines = [KompetensiPenilaianInline]


admin_site.register(Kelas, KelasAdmin)
admin_site.register(MataPelajaranKelas, MataPelajaranKelasAdmin)
