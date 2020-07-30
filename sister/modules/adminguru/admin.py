from django import forms
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import CreateView, DeleteView, UpdateView

from sister.admin.sites import tenant_admin
from sister.admin.views import AdminBaseView

from sister.modules.personal.models import Siswa
from sister.modules.pembelajaran.models import *

from .forms import SiswaPiketForm, RentangNilaiForm, ItemJadwalPelajaranForm

class AdminListView(AdminBaseView):

    model = NotImplemented

    def get_model(self):
        return self.model

    def get_extra_context(self):
        return {
            'object_list': self.model.objects.all()
        }

class AdminDetailView(AdminBaseView):

    model = NotImplementedError

    def get_extra_context(self):
        return {
            'instance': self.object
        }

    def get_model(self):
        return self.model

    def get_object(self):
        object_id = self.kwargs.get('object_id')
        obj = get_object_or_404(self.get_model(), pk=object_id)
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


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
class RentangNilaiUpdateView(UpdateView, AdminBaseView):

    model = RentangNilai
    form_class = RentangNilaiForm
    pk_url_kwarg = 'object_id'
    url_name = 'guruadmin_kelas_rentang_update'
    url_path = 'rentang_nilai/<str:object_id>/update/'
    template_name = 'admin/kelas_rentang_form.html'

    def dispatch(self, request, object_id, *args, **kwargs):
        self.object = get_object_or_404(RentangNilai, pk=object_id)
        return super().dispatch(request, *args, **kwargs)

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
        return "Siswa Kelas %s" % str(self.object)


@tenant_admin.register_view
class KelasDetailPresensi(KelasDetailBase):

    url_name = 'guruadmin_kelas_presensi'
    url_path = 'kelas/<str:object_id>/presensi/'
    template_name = 'admin/kelas_presensi.html'

    def get_page_title(self):
        return "Presensi Kelas %s" % str(self.object)


@tenant_admin.register_view
class KelasDetailMapel(KelasDetailBase):

    url_name = 'guruadmin_kelas_mapel'
    url_path = 'kelas/<str:object_id>/mapel/'
    template_name = 'admin/kelas_mapel.html'

    def get_page_title(self):
        return "Mata Pelajaran Kelas %s" % str(self.object)


@tenant_admin.register_view
class KelasDetailJadwal(KelasDetailBase):

    url_name = 'guruadmin_kelas_jadwal'
    url_path = 'kelas/<str:object_id>/jadwal/'
    template_name = 'admin/kelas_jadwal.html'

    def get_page_title(self):
        return "Jadwal Kelas %s" % str(self.object)


@tenant_admin.register_view
class KelasJadwalAdd(CreateView, AdminBaseView):

    model = ItemJadwalPelajaran
    form_class = ItemJadwalPelajaranForm
    url_name = 'guruadmin_kelas_jadwal_add'
    url_path = 'jadwal_kelas/<str:object_id>/add/'
    template_name = 'admin/kelas_piket_form.html'

    @property
    def media(self):
        js = [
            'vendor/jquery/jquery.js',
            'jquery.init.js',
            'core.js',
            'admin/RelatedObjectLookups.js',
            'actions.min.js',
            'urlify.js',
            'prepopulate.js',
            'vendor/xregexp/xregexp.js',
        ]
        return forms.Media(js=['admin/js/%s' % url for url in js])

    def get_extra_context(self):
        return {'media' : self.media}

    def cancel_url(self):
        return reverse('admin:guruadmin_kelas_jadwal', args=(self.parent.kelas.id,))

    def get_success_url(self):
        return reverse('admin:guruadmin_kelas_jadwal', args=(self.parent.kelas.id,))

    def get_initial(self):
        return {'jadwal_kelas': self.parent}

    def get_page_title(self):
        return "Jadwal Kelas %s" % str(self.parent)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)

    def dispatch(self, request, object_id, *args, **kwargs):
        self.parent = get_object_or_404(JadwalKelas, pk=object_id)
        self.object = None
        return super().dispatch(request, *args, **kwargs)


@tenant_admin.register_view
class KelasDetailPiket(KelasDetailBase):

    url_name = 'guruadmin_kelas_piket'
    url_path = 'kelas/<str:object_id>/piket/'
    template_name = 'admin/kelas_piket.html'

    def get_page_title(self):
        return "Piket Kelas %s" % str(self.object)


@tenant_admin.register_view
class KelasPiketAdd(CreateView, AdminBaseView):

    model = PiketKelas
    form_class = SiswaPiketForm
    url_name = 'guruadmin_kelas_piket_add'
    url_path = 'piket_kelas/<str:piket_id>/add/'
    template_name = 'admin/kelas_piket_form.html'

    def get_initial(self):
        return {'piket_kelas': self.parent}

    def cancel_url(self):
        return reverse('admin:guruadmin_kelas_piket', args=(self.parent.kelas.id,))

    def get_success_url(self):
        return reverse('admin:guruadmin_kelas_piket', args=(self.parent.kelas.id,))

    def get_page_title(self):
        return "Piket Kelas %s" % str(self.parent)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)

    def get_parent(self, piket_id):
        return get_object_or_404(PiketKelas, pk=piket_id)

    def dispatch(self, request, piket_id, *args, **kwargs):
        self.parent = self.get_parent(piket_id)
        self.object = None
        return super().dispatch(request, *args, **kwargs)


@tenant_admin.register_view
class KelasPiketDelete(AdminBaseView):

    model = PiketKelas
    form_class = SiswaPiketForm
    url_name = 'guruadmin_kelas_piket_delete'
    url_path = 'piket_kelas/<str:object_id>/delete/'
    template_name = 'admin/confirm_delete.html'

    def get_success_url(self):
        return reverse('admin:guruadmin_kelas_piket', args=(self.object.piket_kelas.kelas.id,))

    def get_page_title(self):
        return "Hapus Siswa Piket ?"

    def get_parent(self, piket_id):
        return get_object_or_404(PiketKelas, pk=piket_id)

    def get_object(self, object_id):
        return get_object_or_404(ItemPiketKelas, pk=object_id)

    def dispatch(self, request, object_id,*args, **kwargs):
        self.object = self.get_object(object_id)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object.delete()
        return redirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class SiswaDetailBase(AdminDetailView):
    model = Siswa


@tenant_admin.register_view
class SiswaDetail(SiswaDetailBase):

    url_name = 'guruadmin_siswa'
    url_path = 'siswa/<str:object_id>/'
    template_name = 'admin/siswa_detail.html'

    def get_page_title(self):
        return "Siswa %s" % str(self.object)


@tenant_admin.register_view
class SiswaKelasDetail(SiswaDetailBase):

    url_name = 'guruadmin_siswa_kelas'
    url_path = 'siswakelas/<str:object_id>/'
    template_name = 'admin/siswa_kelas.html'

    model = SiswaKelas

    def get_page_title(self):
        return "Siswa %s" % str(self.object)


@tenant_admin.register_view
class SiswaKelasPenilaian(SiswaDetailBase):

    url_name = 'guruadmin_siswa_nilai'
    url_path = 'siswakelas/<str:object_id>/nilai/'
    template_name = 'admin/siswa_nilai.html'

    model = NilaiSiswa

    def get_page_title(self):
        return "Siswa %s" % str(self.object)