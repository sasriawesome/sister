from django.db import transaction
from django.shortcuts import get_object_or_404, reverse, redirect
from sister.admin.sites import tenant_admin
from sister.admin.views import (
    AdminListView, 
    AdminUpdateView,
    AdminDetailView,
    AdminCreateView,
    AdminDeleteView,
    AdminPDFTemplateView
    )

from sister.modules.personal.models import Siswa
from sister.modules.pembelajaran.models import *

from .forms import *


class KelasDetailBase(AdminDetailView):
    model = Kelas


@tenant_admin.register_view
class KelasIndex(AdminListView):

    model = Kelas
    url_name = 'guruadmin_kelas_index'
    url_path = 'kelas/'
    template_name = 'admin/kelas_index.html'

    def get_page_title(self):
        return "Daftar Kelas"


@tenant_admin.register_view
class RentangNilaiUpdate(AdminUpdateView):

    model = RentangNilai
    form_class = RentangNilaiForm
    url_name = 'guruadmin_kelas_rentang_update'
    url_path = 'rentang_nilai/<str:object_id>/update/'
    template_name = 'admin/kelas_rentang_form.html'

    def get_page_title(self):
        return "Update Rentang Nilai %s" % self.object

    def get_success_url(self):
        return reverse('admin:guruadmin_kelas_detail', args=(self.object.kelas.id,))


@tenant_admin.register_view
class KelasDetail(KelasDetailBase):

    url_name = 'guruadmin_kelas_detail'
    url_path = 'kelas/<str:object_id>/'
    template_name = 'admin/kelas_detail.html'

    def get_page_title(self):
        return "Kelas %s" % str(self.object)

    
@tenant_admin.register_view
class KelasDetailSiswa(KelasDetailBase):

    url_name = 'guruadmin_kelas_siswa'
    url_path = 'kelas/<str:object_id>/siswa/'
    template_name = 'admin/kelas_siswa.html'

    def get_page_title(self):
        return "Siswa Kelas: %s" % str(self.object)


@tenant_admin.register_view
class KelasDetailSiswaPrint(AdminPDFTemplateView):
    
    url_name = 'guruadmin_kelas_siswa_print'
    url_path = 'kelas/<str:object_id>/print_siswa'
    template_name = 'admin/prints/kelas_detail_siswa.html'
    header_template = 'admin/print/header_landscape.html'
    cmd_options = {
        'orientation': 'landscape',
        'margin-top': 35,
        'margin-left': 15,
        'margin-right': 15,
        'margin-bottom': 15,
    }

    model = Kelas

    def get_object(self):
        obj_id = self.kwargs.get('object_id')
        obj = get_object_or_404(self.model, pk=obj_id)
        return obj

    def get_extra_context(self):
        return {
            'instance': self.get_object()
        }


@tenant_admin.register_view
class KelasDetailPresensi(KelasDetailBase):

    url_name = 'guruadmin_kelas_presensi'
    url_path = 'kelas/<str:object_id>/presensi/'
    template_name = 'admin/kelas_presensi.html'

    def get_page_title(self):
        return "Presensi Kelas: %s" % str(self.object)


@tenant_admin.register_view
class KelasPresensiAdd(AdminCreateView):

    model = PresensiKelas
    form_class = PresensiKelasForm
    url_name = 'guruadmin_kelas_presensi_add'
    url_path = 'presensi_kelas/<str:object_id>/add/'
    template_name = 'admin/kelas_presensi_form.html'

    def get_success_url(self):
        if self.object and '_save_and_update' in self.request.POST:
            return reverse('admin:guruadmin_kelas_presensi_update', args=(self.object.id,)) 
        return reverse('admin:guruadmin_kelas_presensi', args=(self.parent.id,))

    def get_initial(self):
        return {'kelas': self.parent}

    def get_page_title(self):
        return "Presensi Kelas %s" % str(self.parent)

    def dispatch(self, request, object_id, *args, **kwargs):
        self.parent = get_object_or_404(Kelas, pk=object_id)
        return super().dispatch(request, *args, **kwargs)


@tenant_admin.register_view
class KelasPresensiUpdate(AdminUpdateView):

    model = PresensiKelas
    form_class = PresensiKelasForm
    url_name = 'guruadmin_kelas_presensi_update'
    url_path = 'presensi_kelas/<str:object_id>/update/'
    template_name = 'admin/kelas_presensi_form.html'

    def get_page_title(self):
        return "Presensi Kelas %s" % str(self.object)

    def get_success_url(self):
        if '_save_and_update' in self.request.POST:
            return reverse('admin:guruadmin_kelas_presensi_update', args=(self.object.id,))    
        return reverse('admin:guruadmin_kelas_presensi', args=(self.object.kelas.id,))
    
    def get_initial(self):
        return {'kelas': self.object.kelas}

    def get_extra_context(self):
        extra_context = super().get_extra_context()
        if self.request.POST:
            extra_context.update({
                'inlineform': PresensiSiswaFormSet(
                    self.request.POST or None,
                    instance=self.object)
            })
        else:
            extra_context.update({
                'inlineform': PresensiSiswaFormSet(instance=self.object)
            })
        return extra_context

    def form_valid(self, form=None):
        context = self.get_context_data()
        inlineform = context['inlineform']
        with transaction.atomic():
            self.object = form.save()
            if inlineform.is_valid():
                inlineform.save()
            return super().form_valid(form)

    def dispatch(self, request, object_id, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@tenant_admin.register_view
class KelasPresensiDelete(AdminDeleteView):

    model = PresensiKelas
    url_name = 'guruadmin_kelas_presensi_delete'
    url_path = 'presensi_kelas/<str:object_id>/delete/'
    template_name = 'admin/confirm_delete.html'

    def get_success_url(self):
        return reverse('admin:guruadmin_kelas_presensi', args=(self.object.kelas.id,))

    def get_page_title(self):
        return "Hapus Mata Pelajaran dari Jadwal  ?"


@tenant_admin.register_view
class KelasDetailMapel(KelasDetailBase):

    url_name = 'guruadmin_kelas_mapel'
    url_path = 'kelas/<str:object_id>/mapel/'
    template_name = 'admin/kelas_mapel.html'

    def get_page_title(self):
        return "Mata Pelajaran Kelas: %s" % str(self.object)


@tenant_admin.register_view
class KelasJadwalPelajaran(KelasDetailBase):

    url_name = 'guruadmin_kelas_jadwal'
    url_path = 'kelas/<str:object_id>/jadwal/'
    template_name = 'admin/kelas_jadwal.html'

    def get_page_title(self):
        return "Jadwal Kelas: %s" % str(self.object)


@tenant_admin.register_view
class KelasJadwalPelajaranAdd(AdminCreateView):

    model = JadwalPelajaran
    form_class = JadwalPelajaranForm
    url_name = 'guruadmin_kelas_jadwal_add'
    url_path = 'jadwal_kelas/<str:object_id>/add/'
    template_name = 'admin/base_form.html'

    def get_success_url(self):
        return reverse('admin:guruadmin_kelas_jadwal', args=(self.parent.id,))

    def get_initial(self):
        return {'kelas': self.parent}

    def get_page_title(self):
        return "Tambah Jadwal: %s" % str(self.parent)

    def dispatch(self, request, object_id, *args, **kwargs):
        self.parent = get_object_or_404(Kelas, pk=object_id)
        return super().dispatch(request, *args, **kwargs)


@tenant_admin.register_view
class KelasJadwalPelajaranUpdate(AdminUpdateView):

    model = JadwalPelajaran
    form_class = JadwalPelajaranForm
    url_name = 'guruadmin_kelas_jadwal_update'
    url_path = 'jadwal_kelas/<str:object_id>/update/'
    template_name = 'admin/base_form.html'

    def get_initial(self):
        return {'kelas': self.object.kelas}

    def get_page_title(self):
        return "Update Jadwal: %s" % self.object

    def get_success_url(self):
        return reverse('admin:guruadmin_kelas_jadwal', args=(self.object.kelas.id,))


@tenant_admin.register_view
class KelasJadwalPelajaranPrint(AdminPDFTemplateView):
    
    url_name = 'guruadmin_kelas_jadwal_print'
    url_path = 'kelas/<str:object_id>/print_jadwal'
    template_name = 'admin/prints/kelas_detail_jadwal.html'
    header_template = 'admin/print/header.html'
    cmd_options = {
        'orientation': 'portrait',
        'margin-top': 35,
        'margin-left': 25,
        'margin-right': 25,
        'margin-bottom': 25,
    }

    model = Kelas

    def get_object(self):
        obj_id = self.kwargs.get('object_id')
        obj = get_object_or_404(self.model, pk=obj_id)
        return obj

    def get_extra_context(self):
        return {
            'instance': self.get_object()
        }


@tenant_admin.register_view
class KelasJadwalPelajaranDelete(AdminDeleteView):

    model = JadwalPelajaran
    url_name = 'guruadmin_kelas_jadwal_delete'
    url_path = 'jadwal_kelas/<str:object_id>/delete/'
    template_name = 'admin/confirm_delete.html'

    def get_success_url(self):
        return reverse('admin:guruadmin_kelas_jadwal', args=(self.object.kelas.id,))

    def get_page_title(self):
        return "Hapus Mata Pelajaran dari Jadwal  ?"


@tenant_admin.register_view
class KelasPiketSiswa(KelasDetailBase):

    url_name = 'guruadmin_kelas_piket'
    url_path = 'kelas/<str:object_id>/piket/'
    template_name = 'admin/kelas_piket.html'

    def get_page_title(self):
        return "Piket Kelas: %s" % str(self.object)


@tenant_admin.register_view
class KelasPiketSiswaAdd(AdminCreateView):

    model = JadwalPiketSiswa
    form_class = JadwalPiketSiswaForm
    url_name = 'guruadmin_kelas_piket_add'
    url_path = 'piket_kelas/<str:object_id>/add/'
    template_name = 'admin/base_form.html'

    def get_initial(self):
        return {'kelas': self.parent}

    def get_success_url(self):
        return reverse('admin:guruadmin_kelas_piket', args=(self.parent.id,))

    def get_page_title(self):
        return "Tambah Siswa Piket: %s" % str(self.parent)

    def dispatch(self, request, object_id, *args, **kwargs):
        self.parent = get_object_or_404(Kelas, pk=object_id)
        return super().dispatch(request, *args, **kwargs)


@tenant_admin.register_view
class KelasPiketSiswaDelete(AdminDeleteView):

    model = JadwalPiketSiswa
    url_name = 'guruadmin_kelas_piket_delete'
    url_path = 'piket_kelas/<str:object_id>/delete/'
    template_name = 'admin/confirm_delete.html'

    def get_success_url(self):
        return reverse('admin:guruadmin_kelas_piket', args=(self.object.kelas.id,))

    def get_page_title(self):
        return "Hapus Siswa Piket ?"


@tenant_admin.register_view
class KelasPiketPrint(AdminPDFTemplateView):
    
    url_name = 'guruadmin_kelas_piket_print'
    url_path = 'kelas/<str:object_id>/print_piket'
    template_name = 'admin/prints/kelas_detail_piket.html'
    header_template = 'admin/print/header.html'
    cmd_options = {
        'orientation': 'portrait',
        'margin-top': 35,
        'margin-left': 25,
        'margin-right': 25,
        'margin-bottom': 25,
    }

    model = Kelas

    def get_object(self):
        obj_id = self.kwargs.get('object_id')
        obj = get_object_or_404(self.model, pk=obj_id)
        return obj

    def get_extra_context(self):
        return {
            'instance': self.get_object()
        }


class SiswaDetailBase(AdminDetailView):
    model = Siswa


@tenant_admin.register_view
class SiswaDetail(SiswaDetailBase):

    url_name = 'guruadmin_siswa'
    url_path = 'siswa/<str:object_id>/'
    template_name = 'admin/siswa_detail.html'

    def get_page_title(self):
        return "Profil Siswa: %s" % str(self.object)


@tenant_admin.register_view
class SiswaKelasDetail(SiswaDetailBase):

    model = SiswaKelas
    url_name = 'guruadmin_siswa_kelas'
    url_path = 'siswakelas/<str:object_id>/'
    template_name = 'admin/siswa_kelas.html'

    def get_page_title(self):
        return "Siswa Kelas: %s" % str(self.object)


@tenant_admin.register_view
class SiswaKelasPenilaian(SiswaDetailBase):

    model = NilaiSiswa
    url_name = 'guruadmin_siswa_nilai'
    url_path = 'siswakelas/<str:object_id>/nilai/'
    template_name = 'admin/siswa_nilai.html'

    def get_page_title(self):
        return "Siswa: %s" % str(self.object)