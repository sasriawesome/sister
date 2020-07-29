from django.contrib import admin
from django.shortcuts import reverse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from sister.core import hooks
from sister.admin.sites import tenant_admin
from sister.admin.admin import ModelAdmin, ModelMenuGroup

from .models import *


class MataPelajaranKelasInline(admin.TabularInline):
    extra = 1
    exclude = ['kkm', 'tugas', 'ph', 'pts', 'pas']
    model = MataPelajaranKelas


class ItemJadwalPelajaranInline(admin.TabularInline):
    extra = 1
    model = ItemJadwalPelajaran


class ItemJadwalEkstraKurikulerInline(admin.TabularInline):
    extra = 0
    model = ItemJadwalEkstraKurikuler


class JadwalKelasAdmin(ModelAdmin):
    inlines = [
        ItemJadwalPelajaranInline,
        ItemJadwalEkstraKurikulerInline
        ]


class ItemPiketKelasInline(admin.TabularInline):
    extra = 1
    model = ItemPiketKelas


class PiketKelasAdmin(ModelAdmin):
    inlines = [ItemPiketKelasInline]


class SiswaKelasInline(admin.TabularInline):
    extra = 1
    model = SiswaKelas


class KelasAdmin(ModelAdmin):
    inlines = [MataPelajaranKelasInline, SiswaKelasInline]

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = []

        # Need Validation
        custom_urls.append(
            path('<path:object_id>/rentang_nilai/',
                self.admin_site.admin_view(self.rentang_view),
                name='%s_%s_rentang_view' % (self.opts.app_label, self.opts.model_name)
            )
        )

        # Need Validation
        custom_urls.append(
            path('<path:object_id>/mata_pelajaran/',
                self.admin_site.admin_view(self.mapel_view),
                name='%s_%s_mapel_view' % (self.opts.app_label, self.opts.model_name)
            )
        )

        # Need Validation
        custom_urls.append(
            path('<path:object_id>/jadwal/',
                self.admin_site.admin_view(self.jadwal_view),
                name='%s_%s_jadwal_view' % (self.opts.app_label, self.opts.model_name)
            )
        )

        # Need Validation
        custom_urls.append(
            path('<path:object_id>/piket/',
                self.admin_site.admin_view(self.piket_view),
                name='%s_%s_piket_view' % (self.opts.app_label, self.opts.model_name)
            )
        )

        # Need Validation
        custom_urls.append(
            path('<path:object_id>/presensi/',
                self.admin_site.admin_view(self.presensi_view),
                name='%s_%s_presensi_view' % (self.opts.app_label, self.opts.model_name)
            )
        )

        # Need Validation
        custom_urls.append(
            path('<path:object_id>/siswa_kelas/',
                self.admin_site.admin_view(self.siswa_kelas_view),
                name='%s_%s_siswakelas_view' % (self.opts.app_label, self.opts.model_name)
            )
        )

        return custom_urls + urls

    def get_inspect_context(self, obj, request, extra_context=None):
        context = {
            **self.admin_site.each_context(request),
            'self': self,
            'opts': self.opts,
            'instance': obj,
            **(extra_context or {})
        }
        return context

    def siswa_kelas_view(self, request, object_id, extra_context=None):
        template = 'admin/%s/%s/siswa_kelas.html' % (self.opts.app_label, self.opts.model_name)
        obj = self.get_object(request, object_id)
        context = self.get_inspect_context(obj, request)
        # if not self.has_view_or_change_permission(request, obj):
        #     return PermissionError("You don't have any permissions")
        context = self.get_inspect_context(obj, request, extra_context)
        return TemplateResponse(request, template, context)

    def rentang_view(self, request, object_id, extra_context=None):
        template = 'admin/%s/%s/rentang_nilai.html' % (self.opts.app_label, self.opts.model_name)
        obj = self.get_object(request, object_id)
        context = self.get_inspect_context(obj, request)
        # if not self.has_view_or_change_permission(request, obj):
        #     return PermissionError("You don't have any permissions")
        context = self.get_inspect_context(obj, request, extra_context)
        return TemplateResponse(request, template, context)

    def mapel_view(self, request, object_id, extra_context=None):
        template = 'admin/%s/%s/mata_pelajaran.html' % (self.opts.app_label, self.opts.model_name)
        obj = self.get_object(request, object_id)
        context = self.get_inspect_context(obj, request)
        # if not self.has_view_or_change_permission(request, obj):
        #     return PermissionError("You don't have any permissions")
        context = self.get_inspect_context(obj, request, extra_context)
        return TemplateResponse(request, template, context)

    def jadwal_view(self, request, object_id, extra_context=None):
        template = 'admin/%s/%s/jadwal.html' % (self.opts.app_label, self.opts.model_name)
        obj = self.get_object(request, object_id)
        context = self.get_inspect_context(obj, request)
        # if not self.has_view_or_change_permission(request, obj):
        #     return PermissionError("You don't have any permissions")
        context = self.get_inspect_context(obj, request, extra_context)
        return TemplateResponse(request, template, context)

    def piket_view(self, request, object_id, extra_context=None):
        template = 'admin/%s/%s/piket.html' % (self.opts.app_label, self.opts.model_name)
        obj = self.get_object(request, object_id)
        context = self.get_inspect_context(obj, request)
        # if not self.has_view_or_change_permission(request, obj):
        #     return PermissionError("You don't have any permissions")
        context = self.get_inspect_context(obj, request, extra_context)
        return TemplateResponse(request, template, context)

    def presensi_view(self, request, object_id, extra_context=None):
        template = 'admin/%s/%s/presensi.html' % (self.opts.app_label, self.opts.model_name)
        obj = self.get_object(request, object_id)
        context = self.get_inspect_context(obj, request)
        # if not self.has_view_or_change_permission(request, obj):
        #     return PermissionError("You don't have any permissions")
        context = self.get_inspect_context(obj, request, extra_context)
        return TemplateResponse(request, template, context)


class RentangNilaiAdmin(ModelAdmin):
    list_display = ['kelas', 'nilai_minimum', 'nilai_maximum', 'predikat', 'aksi']


class NilaiMataPelajaranK13Inline(admin.StackedInline):
    extra = 1
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
    extra = 1
    model = PresensiSiswa


class PresensiKelasAdmin(ModelAdmin):
    list_filter = ['kelas']
    inlines = [PresensiSiswa]

    def get_inlines(self, request, obj):
        if obj:
            return self.inlines
        return []


tenant_admin.register(Kelas, KelasAdmin)
tenant_admin.register(JadwalKelas, JadwalKelasAdmin)
tenant_admin.register(PiketKelas, PiketKelasAdmin)
tenant_admin.register(NilaiSiswa, NilaiSiswaAdmin)
tenant_admin.register(RentangNilai, RentangNilaiAdmin)
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