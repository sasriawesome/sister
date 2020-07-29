from django.shortcuts import get_object_or_404

from sister.admin.sites import tenant_admin
from sister.admin.views import AdminBaseView

from sister.modules.personal.models import Siswa
from sister.modules.pembelajaran.models import Kelas, SiswaKelas, NilaiSiswa


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
class KelasDetail(KelasDetailBase):

    url_name = 'guruadmin_kelas'
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
class KelasDetailPiket(KelasDetailBase):

    url_name = 'guruadmin_kelas_piket'
    url_path = 'kelas/<str:object_id>/piket/'
    template_name = 'admin/kelas_piket.html'

    def get_page_title(self):
        return "Piket Kelas %s" % str(self.object)


@tenant_admin.register_view
class KelasDetailRentang(KelasDetailBase):

    url_name = 'guruadmin_kelas_rentang'
    url_path = 'kelas/<str:object_id>/rentang/'
    template_name = 'admin/kelas_rentang.html'

    def get_page_title(self):
        return "Rentang Nilai %s" % str(self.object)

    
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