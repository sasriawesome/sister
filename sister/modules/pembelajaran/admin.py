from django.contrib import admin

# from sister.core import hooks
from sister.admin.sites import tenant_admin
from sister.admin.admin import ModelAdmin

from .models import (
    Kelas,
    MataPelajaranKelas,
    JadwalPelajaran,
    JadwalPiketSiswa,
    SiswaKelas,
    RentangNilai
)


class TahunAjaranAdmin(ModelAdmin):
    pass


class MataPelajaranKelasInline(admin.TabularInline):
    extra = 1
    exclude = ['kkm', 'tugas', 'ph', 'pts', 'pas']
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
        'tahun_ajaran',
        'kurikulum'
        ]
    list_select_related = ['guru_kelas', 'tahun_ajaran', 'kurikulum']
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


tenant_admin.register(Kelas, KelasAdmin)


# class PersonalModelMenuGroup(ModelMenuGroup):
#     adminsite = admin.site
#     menu_label = _('Personals')
#     menu_icon = 'account'
#     items = [
#         (Person, PersonAdmin),
#         (Siswa, SiswaAdmin),
#         (Wali, WaliAdmin),
#         (Guru, GuruAdmin),
#         (Kelas, PersonAdmin),
#     ]


# class KelasModelMenuGroup(ModelMenuGroup):
#     adminsite = admin.site
#     menu_label = _('Classrooms')
#     menu_icon = 'teach'
#     items = [
#         (JadwalPelajaran, JadwalPelajaranAdmin),
#         (RentangNilai, RentangNilaiAdmin),
#         (PresensiSiswa , PresensiSiswaAdmin),
#         (PenilaianMataPelajaran , PenilaianMataPelajaranAdmin),
#         (PenilaianEkstraKurikuler , PenilaianEkstraKurikulerAdmin),
#     ]


# class KurikulumModelMenuGroup(ModelMenuGroup):
#     adminsite = admin.site
#     menu_label = _('Curriculum')
#     menu_icon = 'book'
#     items = [
#         (Tema, TemaAdmin),
#         (Sekolah, SekolahAdmin),
#         (TahunAjaran, TahunAjaranAdmin),
#         (Kurikulum, KurikulumAdmin),
#         (MataPelajaran, MataPelajaranAdmin),
#         (KompetensiInti, KompetensiIntiAdmin),
#         (KompetensiDasar, KompetensiDasarAdmin),
#     ]


# @hooks.register('admin_menu_item')
# def register_kurikulum_menu(request):
#     group = KurikulumModelMenuGroup()
#     return group.get_menu_item(request)


# @hooks.register('admin_menu_item')
# def register_personal_menu(request):
#     group = PersonalModelMenuGroup()
#     return group.get_menu_item(request)


# @hooks.register('admin_menu_item')
# def register_kelas_menu(request):
#     group = KelasModelMenuGroup()
#     return group.get_menu_item(request)
