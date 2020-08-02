from django.contrib import admin
from django.shortcuts import reverse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from sister.core import hooks
from sister.admin.sites import tenant_admin
from sister.admin.admin import ModelAdmin, ModelMenuGroup

from .models import *

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
    search_fields = ['nama_kelas', 'guru_kelas__nip', 'guru_kelas__person__full_name']
    list_display = ['nama_kelas', 'guru_kelas', 'tahun_ajaran', 'kurikulum']
    list_select_related = ['guru_kelas', 'tahun_ajaran', 'kurikulum']
    inlines = [
        MataPelajaranKelasInline,
        SiswaKelasInline,
        JadwalPelajaranInline,
        JadwalPiketSiswaInline,
        ]

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return [ *list_display, 'view_link']

    def view_link(self, obj):
        template = "<a class='viewlink' href='%s' title='%s'></a>"
        url = reverse('admin:guruadmin_kelas_detail', args=(obj.id,))
        return format_html(template % (url, _('inspect').title()))

    view_link.short_description=''


class RentangNilaiAdmin(ModelAdmin):
    list_display = ['kelas', 'nilai_minimum', 'nilai_maximum', 'predikat', 'aksi']


class NilaiMataPelajaranK13Inline(admin.StackedInline):
    extra = 0
    model = NilaiMataPelajaranK13


class NilaiSiswaAdmin(ModelAdmin):
    inlines = [
        NilaiMataPelajaranK13Inline
        ]

class NilaiSiswaKTSPAdmin(ModelAdmin):
    list_display = [
        'siswa', 
        'mata_pelajaran', 
        'nilai', 
        'deskripsi', 
        ]


class NilaiSiswaK13Admin(ModelAdmin):
    list_display = [
        'siswa', 
        'mata_pelajaran', 
        'nilai_spiritual', 
        'nilai_sosial', 
        'nilai_pengetahuan', 
        'nilai_keterampilan'
        ]


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

tenant_admin.register(TahunAjaran, TahunAjaranAdmin)
tenant_admin.register(Kelas, KelasAdmin)
tenant_admin.register(NilaiSiswa, NilaiSiswaAdmin)
tenant_admin.register(PresensiKelas, PresensiKelasAdmin)


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