from django.db import transaction
from django.forms import inlineformset_factory
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import reverse, get_object_or_404, Http404
from django.utils.translation import gettext_lazy as _
from graphene.relay import Node
from sister_api.views import GrapheneView
from sister_api.tenant.v1 import schema

from sister.modules.personal.models import (
    Person
)
from sister.modules.pembelajaran.models import (
    Kelas,
    SiswaKelas,
    MataPelajaranKelas,
    JadwalPelajaran,
    JadwalPiketSiswa,
    RentangNilai
)
from sister.modules.presensi.models import (
    PresensiKelas,
    PresensiSiswa,
)
from sister.modules.penilaian.models import (
    PenilaianPembelajaran
)
from .forms import (
    JadwalPelajaranForm,
    JadwalPiketSiswaForm,
    PresensiKelasForm,
    PresensiSiswaForm,
    RentangNilaiForm
)

from .sites import website
from .options import (
    WebContextMixin,
    WebViewMixin,
    WebView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class BaseGrapheneView(WebViewMixin, GrapheneView, WebContextMixin):
    pass


# @website.register
# class IndexView(WebView):
#     url_path = ''
#     url_name = 'index'
#     template_name = 'sister_web/pages/index.html'

#     def get_extra_context(self):
#         guru = getattr(self.request.user, 'guru', None)
#         kelas_filters = {}
#         mapel_filters = {}
#         if guru:
#             kelas_filters = {
#                 'guru_kelas': guru
#             }
#             mapel_filters = {
#                 'guru': guru
#             }
#         return {
#             'kelas': Kelas.objects.filter(**kelas_filters),
#             'mapel': MataPelajaranKelas.objects.filter(**mapel_filters)
#         }


@website.register
class ProfileView(WebView):
    url_path = 'profile/'
    url_name = 'profile'
    template_name = 'sister_web/pages/profil.html'

    def get_backurl(self):
        return reverse('sister_web_index')

    def get_context_data(self):
        extra_context = {
            'page_title': 'Profile',
            'backurl': self.get_backurl(),
            'instance': self.request.user.profile
        }
        profile_id = self.request.GET.get('profile_id', None)
        if profile_id:
            try:
                profile = Person.objects.get(pk=profile_id)
                extra_context.update({
                    'instance': profile
                })
            except Person.DoesNotExist:
                pass
        return extra_context


@website.register
class IndexView(BaseGrapheneView):
    schema = schema
    url_path = ''
    url_name = 'index'
    operation = 'guru'
    template_name = 'sister_web/pages/index.html'
    query = """
        query getGuru($id: ID!){
            guru(id:$id) {
                
            }
        }
    """

    def get_backurl(self):
        return reverse('sister_web_index')

    def get_extra_context(self):
        guru = getattr(self.request.user, 'guru', None)
        kelas_filters = {}
        mapel_filters = {}
        if guru:
            kelas_filters = {
                'guru_kelas': guru
            }
            mapel_filters = {
                'guru': guru
            }
        return {
            'kelas': Kelas.objects.filter(**kelas_filters),
            'mapel': MataPelajaranKelas.objects.filter(**mapel_filters)
        }


@website.register
class KelasView(BaseGrapheneView):
    schema = schema
    url_name = 'kelas'
    url_path = 'kelas/<str:id>/'
    template_name = 'sister_web/pages/kelas.html'
    operation = 'kelas'
    query = """
        query getKelas($id: ID!){
            kelas(id:$id) {
            id
            modifiedAt
            createdAt
            namaKelas
            kelas
            kurikulum {
                id
                kode
                nama
            }
            tahunAjaran {
                id
                kode
            }
            guruKelas {
                id
                person {
                id
                pid
                fullName
                title
                photoSet {
                edges {
                    node {
                    photo
                    primary
                    }
                }
                }
                }
                nip
            }
            ruang {
                kode
                nama
            }
            semester
            status
            }
        }
    """

    def get_extra_context(self):
        extra_context = {
            'backurl': reverse('sister_web_index'),
            'page_title': "%s" % str(self.object),
            'menu_list': self.get_menu_list()
        }
        return extra_context

    def get_menu_list(self):
        return [
            {
                'url': reverse(
                    'sister_web_kelas_siswa_list', args=(self.object.id,)),
                'icon': 'user-graduate',
                'title': 'Siswa Kelas',
                'description': 'Daftar dan profil Siswa Kelas.'
            }, {
                'url': reverse(
                    'sister_web_kelas_mapel_list', args=(self.object.id,)),
                'icon': 'book',
                'title': 'Mata Pelajaran',
                'description': 'Daftar Mata Pelajaran Kelas.'
            }, {
                'url': reverse(
                    'sister_web_kelas_jadwal_list', args=(self.object.id,)),
                'icon': 'calendar-alt',
                'title': 'Jadwal Pelajaran',
                'description': 'Daftar jadwal Mata Pelajaran dalam seminggu.'
            }, {
                'url': reverse(
                    'sister_web_kelas_piket_list', args=(self.object.id,)),
                'icon': 'calendar',
                'title': 'Piket Kelas',
                'description': 'Daftar Piket siswa dalam seminggu.'
            }, {
                'url': reverse(
                    'sister_web_kelas_absensi_list', args=(self.object.id,)),
                'icon': 'hand-sparkles',
                'title': 'Absensi Kelas',
                'description': 'Daftar absensi siswa harian.'
            }, {
                'url': reverse(
                    'sister_web_kelas_rentang_list', args=(self.object.id,)),
                'icon': 'bookmark',
                'title': 'Rentang Penilaian',
                'description': 'Rentan dan predikat penilaian.'
            }, {
                # 'url': reverse('', args=(self.object.id,)),
                'icon': 'chalkboard',
                'title': 'Buku Kelas',
                'description': 'Laporan Buku Kelas'
            }, {
                # 'url': reverse('', args=(self.object.id,)),
                'icon': 'graduation-cap',
                'title': 'Raport Siswa',
                'description': 'Hasil belajar dan Buku Raport Siswa.'
            }
        ]

# @website.register
# class KelasView(DetailView):
#     model = Kelas
#     url_path = 'kelas/<str:object_id>/'
#     url_name = 'kelas'
#     template_name = 'sister_web/pages/kelas.html'

#     def get_backurl(self):
#         return reverse('sister_web_index')

#     def get_menu_list(self):
#         return [
#             {
#                 'url': reverse(
#                     'sister_web_kelas_siswa_list', args=(self.object.id,)),
#                 'icon': 'user-graduate',
#                 'title': 'Siswa Kelas',
#                 'description': 'Daftar dan profil Siswa Kelas.'
#             }, {
#                 'url': reverse(
#                     'sister_web_kelas_mapel_list', args=(self.object.id,)),
#                 'icon': 'book',
#                 'title': 'Mata Pelajaran',
#                 'description': 'Daftar Mata Pelajaran Kelas.'
#             }, {
#                 'url': reverse(
#                     'sister_web_kelas_jadwal_list', args=(self.object.id,)),
#                 'icon': 'calendar-alt',
#                 'title': 'Jadwal Pelajaran',
#                 'description': 'Daftar jadwal Mata Pelajaran dalam seminggu.'
#             }, {
#                 'url': reverse(
#                     'sister_web_kelas_piket_list', args=(self.object.id,)),
#                 'icon': 'calendar',
#                 'title': 'Piket Kelas',
#                 'description': 'Daftar Piket siswa dalam seminggu.'
#             }, {
#                 'url': reverse(
#                     'sister_web_kelas_absensi_list', args=(self.object.id,)),
#                 'icon': 'hand-sparkles',
#                 'title': 'Absensi Kelas',
#                 'description': 'Daftar absensi siswa harian.'
#             }, {
#                 'url': reverse(
#                     'sister_web_kelas_rentang_list', args=(self.object.id,)),
#                 'icon': 'bookmark',
#                 'title': 'Rentang Penilaian',
#                 'description': 'Rentan dan predikat penilaian.'
#             }, {
#                 # 'url': reverse('', args=(self.object.id,)),
#                 'icon': 'chalkboard',
#                 'title': 'Buku Kelas',
#                 'description': 'Laporan Buku Kelas'
#             }, {
#                 # 'url': reverse('', args=(self.object.id,)),
#                 'icon': 'graduation-cap',
#                 'title': 'Raport Siswa',
#                 'description': 'Hasil belajar dan Buku Raport Siswa.'
#             }
#         ]

#     def get_extra_context(self):
#         extra_context = {
#                 'backurl': reverse('sister_web_index'),
#                 'page_title': self.get_page_title(),
#                 'menu_list': self.get_menu_list()
#             }
#         return extra_context

#     def get_page_title(self):
#         page_mode = self.request.GET.get('page_mode', 'Kelas')
#         return "%s %s" % (page_mode.title(), str(self.object))


@website.register
class MapelKelasList(DetailView):
    model = Kelas
    url_path = 'kelas/<str:object_id>/mapel/'
    url_name = 'kelas_mapel_list'
    template_name = 'sister_web/pages/kelas_mapel_list.html'

    def get_backurl(self):
        return reverse('sister_web_kelas', args=(self.object.id,))

    def get_object_list(self):
        # TODO cache
        return self.object.mata_pelajaran_kelas.all()

    def get_extra_context(self):
        semester_mode = self.request.GET.get('semester', 1)
        if int(semester_mode) != 1:
            semester_mode = 2
        extra_context = {
            'page_title': self.get_page_title(),
            'semester': semester_mode,
            'object_list': self.get_object_list()
        }
        return extra_context

    def get_page_title(self):
        return "%s %s" % ('Pelajaran', str(self.object))


@website.register
class MapelKelasDetail(DetailView):
    model = MataPelajaranKelas
    url_name = 'mapelkelas'
    url_path = 'mapelkelas/<str:object_id>/'
    template_name = 'sister_web/pages/kelas_mapel_detail.html'

    def get_backurl(self):
        if self.origin == 'index':
            return reverse('sister_web_index')
        else:
            return reverse(
                'sister_web_kelas_mapel_list',
                args=(self.object.kelas.id,)
            )

    def get_extra_context(self):
        self.origin = self.request.GET.get('origin', 'mapel')
        extra_context = super().get_extra_context()
        extra_context.update({
            'origin': self.origin
        })
        return extra_context

    def get_page_title(self):
        return "Mapel %s" % self.object.kelas


@website.register
class MapelKelasPenilaian(WebView):
    page_title = 'Penilaian Pembelajaran'
    url_path = 'mapelkelas/<str:mapel_id>/' \
               'siswakelas/<str:siswa_id>/' \
               'penilaian_semester/<int:semester>/'
    url_name = 'mapelkelas_penilaian'
    template_name = 'sister_web/pages/kelas_mapel_penilaian.html'

    def get_backurl(self):
        origin = self.request.GET.get('origin', 'kelas')
        if origin == 'siswa':
            return reverse('sister_web_siswakelas', args=(self.siswa.id,))
        else:
            url = reverse('sister_web_mapelkelas', args=(self.mapel.id,))
            ori = "?origin=%s" % origin
            return url + ori if origin == 'index' else url

    def get_object(self, mapel_id, siswa_id, semester):
        self.mapel = get_object_or_404(MataPelajaranKelas, pk=mapel_id)
        self.siswa = get_object_or_404(SiswaKelas, pk=siswa_id)
        valid_semester = semester if semester in [1, 2] else 1
        defaults = {
            'mata_pelajaran': self.mapel,
            'siswa': self.siswa,
            'semester': valid_semester
        }
        instance, created = PenilaianPembelajaran.objects.get_or_create(
            **defaults, defaults=defaults
        )
        return instance

    def get(self, request, mapel_id, siswa_id, semester, *args, **kwargs):
        self.object = self.get_object(mapel_id, siswa_id, semester)
        context = self.get_context_data(instance=self.object)
        return self.render_to_response(context)


@website.register
class SiswaKelasList(DetailView):
    model = Kelas
    url_path = 'kelas/<str:object_id>/siswa/'
    url_name = 'kelas_siswa_list'
    template_name = 'sister_web/pages/kelas_siswa_list.html'

    def get_backurl(self):
        return reverse('sister_web_kelas', args=(self.object.id,))

    def get_object_list(self):
        # TODO cache
        return self.object.siswa.all()

    def get_extra_context(self):
        semester_mode = self.request.GET.get('semester', 1)
        if int(semester_mode) != 1:
            semester_mode = 2
        extra_context = {
            'page_title': self.get_page_title(),
            'semester': semester_mode,
            'object_list': self.get_object_list()
        }
        return extra_context

    def get_page_title(self):
        return "%s %s" % ('Siswa', str(self.object))


@website.register
class SiswaKelasDetail(DetailView):
    model = SiswaKelas
    url_name = 'siswakelas'
    url_path = 'siswakelas/<str:object_id>/'
    template_name = 'sister_web/pages/kelas_siswa_detail.html'

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_siswa_list',
            args=(self.object.kelas.id,)
        )

    def get_page_title(self):
        return "Siswa %s" % self.object.kelas


@website.register
class JadwalPelajaranList(DetailView):
    model = Kelas
    url_path = 'kelas/<str:object_id>/jadwal/'
    url_name = 'kelas_jadwal_list'
    template_name = 'sister_web/pages/kelas_jadwal.html'

    def get_backurl(self):
        return reverse('sister_web_kelas', args=(self.object.id,))

    def get_object_list(self, semester):
        # TODO cache
        return self.object.jadwal_pelajaran.filter(semester=semester)

    def get_extra_context(self):
        semester = self.request.GET.get('semester', 1)
        if int(semester) != 1:
            semester = 2
        extra_context = {
            'page_title': self.get_page_title(),
            'semester': int(semester),
            'object_list': self.get_object_list(int(semester))
        }
        return extra_context

    def get_page_title(self):
        return "%s %s" % ('Jadwal', str(self.object))


@website.register
class JadwalPelajaranCreate(CreateView):

    model = JadwalPelajaran
    form_class = JadwalPelajaranForm
    url_name = 'kelas_jadwal'
    url_path = 'kelas_jadwal_pelajaran/<str:object_id>/create/'

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_jadwal_list',
            args=(self.parent.id,)
        )

    def get_success_url(self):
        return reverse(
            'sister_web_kelas_jadwal_list',
            args=(self.parent.id,)
        ) + "?semester=%s" % self.object.semester

    def get_initial(self):
        return {'kelas': self.parent}

    def get_page_title(self):
        return "Form Jadwal Pelajaran"

    def dispatch(self, request, object_id, *args, **kwargs):
        self.parent = get_object_or_404(Kelas, pk=object_id)
        return super().dispatch(request, *args, **kwargs)


@website.register
class JadwalPelajaranChange(UpdateView):

    model = JadwalPelajaran
    form_class = JadwalPelajaranForm
    url_name = 'kelas_jadwal_update'
    url_path = 'kelas_jadwal_pelajaran/<str:object_id>/update/'

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_jadwal_list',
            args=(self.object.kelas.id,)
        )

    def get_success_url(self):
        return reverse(
            'sister_web_kelas_jadwal_list',
            args=(self.object.kelas.id,)
        ) + "?semester=%s" % self.object.semester

    def get_initial(self):
        return {'kelas': self.object.kelas}

    def get_page_title(self):
        return "Form Jadwal Pelajaran"


@website.register
class JadwalPelajaranDelete(DeleteView):

    model = JadwalPelajaran
    form_class = JadwalPelajaranForm
    url_name = 'kelas_jadwal_delete'
    url_path = 'kelas_jadwal_pelajaran/<str:object_id>/delete/'

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_jadwal_list',
            args=(self.object.kelas.id,)
        )

    def get_success_url(self):
        return reverse(
            'sister_web_kelas_jadwal_list',
            args=(self.object.kelas.id,)
        ) + "?semester=%s" % self.object.semester

    def get_page_title(self):
        return "Konfirmasi"


@website.register
class JadwalPiketList(DetailView):
    model = Kelas
    url_path = 'kelas/<str:object_id>/piket/'
    url_name = 'kelas_piket_list'
    template_name = 'sister_web/pages/kelas_piket.html'

    def get_backurl(self):
        return reverse('sister_web_kelas', args=(self.object.id,))

    def get_object_list(self, semester):
        # TODO cache
        return self.object.piket.filter(semester=semester)

    def get_extra_context(self):
        semester = self.request.GET.get('semester', 1)
        if int(semester) != 1:
            semester = 2
        extra_context = {
            'page_title': self.get_page_title(),
            'semester': int(semester),
            'object_list': self.get_object_list(int(semester))
        }
        return extra_context

    def get_page_title(self):
        return "%s %s" % ('Piket', str(self.object))


@website.register
class JadwalPiketCreate(CreateView):

    model = JadwalPiketSiswa
    form_class = JadwalPiketSiswaForm
    url_name = 'kelas_piket'
    url_path = 'kelas_jadwal_piket/<str:object_id>/create/'

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_piket_list',
            args=(self.parent.id,)
        )

    def get_success_url(self):
        return reverse(
            'sister_web_kelas_piket_list',
            args=(self.parent.id,)
        ) + "?semester=%s" % self.object.semester

    def get_initial(self):
        return {'kelas': self.parent}

    def get_page_title(self):
        return "Form Jadwal Piket"

    def dispatch(self, request, object_id, *args, **kwargs):
        self.parent = get_object_or_404(Kelas, pk=object_id)
        return super().dispatch(request, *args, **kwargs)


@website.register
class JadwalPiketUpdate(UpdateView):

    model = JadwalPiketSiswa
    form_class = JadwalPiketSiswaForm
    url_name = 'kelas_piket_update'
    url_path = 'kelas_jadwal_piket/<str:object_id>/update/'

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_piket_list',
            args=(self.object.kelas.id,)
        )

    def get_success_url(self):
        return reverse(
            'sister_web_kelas_piket_list',
            args=(self.object.kelas.id,)
        ) + "?semester=%s" % self.object.semester

    def get_initial(self):
        return {'kelas': self.object.kelas}

    def get_page_title(self):
        return "Form Jadwal Kelas"


@website.register
class JadwalPiketDelete(DeleteView):

    model = JadwalPiketSiswa
    form_class = JadwalPiketSiswaForm
    url_name = 'kelas_piket_delete'
    url_path = 'kelas_jadwal_piket/<str:object_id>/delete/'

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_piket_list',
            args=(self.object.kelas.id,)
        )

    def get_success_url(self):
        return reverse(
            'sister_web_kelas_piket_list',
            args=(self.object.kelas.id,)
        ) + "?semester=%s" % self.object.semester

    def get_page_title(self):
        return "Konfirmasi"


@website.register
class AbsensiList(DetailView):
    model = Kelas
    per_page = 7
    url_path = 'kelas/<str:object_id>/absensi/'
    url_name = 'kelas_absensi_list'
    template_name = 'sister_web/pages/kelas_absensi.html'

    def get_backurl(self):
        return reverse('sister_web_kelas', args=(self.object.id,))

    def paginate(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = Paginator(queryset, page_size, allow_empty_first_page=True)
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_(
                    'Page is not “last”, nor can it be converted to an int.'
                ))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_object_list(self, semester):
        return self.object.presensi.filter(semester=semester)

    def get_extra_context(self):
        semester = self.request.GET.get('semester', 1)
        qs = self.get_object_list(semester=semester)
        if int(semester) != 1:
            semester = 2
        paginator, page, queryset, paginated = self.paginate(qs, 7)
        extra_context = {
            'page_title': self.get_page_title(),
            'semester': int(semester),
            'is_paginated': paginated,
            'object_list': queryset,
            'paginator': paginator,
            'page_obj': page
        }
        return extra_context

    def get_page_title(self):
        return "%s %s" % ('Absensi', str(self.object))


@website.register
class AbsensiCreate(CreateView):

    model = PresensiKelas
    form_class = PresensiKelasForm
    url_name = 'kelas_absensi'
    url_path = 'kelas_absensi/<str:object_id>/create/'

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_absensi_list',
            args=(self.parent.id,)
        )

    def get_success_url(self):
        if '_save_and_update' in self.request.POST:
            return reverse(
                'sister_web_kelas_absensi_update',
                args=(self.object.id,)
            )
        return reverse(
            'sister_web_kelas_absensi_list',
            args=(self.parent.id,)
        ) + "?semester=%s" % self.object.semester

    def get_initial(self):
        return {'kelas': self.parent}

    def get_page_title(self):
        return "Form Absensi Siswa"

    def dispatch(self, request, object_id, *args, **kwargs):
        self.parent = get_object_or_404(Kelas, pk=object_id)
        return super().dispatch(request, *args, **kwargs)


@website.register
class AbsensiUpdate(UpdateView):

    model = PresensiKelas
    form_class = PresensiKelasForm
    url_name = 'kelas_absensi_update'
    url_path = 'kelas_absensi/<str:object_id>/update/'
    inline_fields = ['siswa', 'keterangan']

    def get_page_title(self):
        return "Form Absensi Siswa"

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_absensi_list',
            args=(self.object.kelas.id,)
        ) + "?semester=%s" % self.object.semester

    def get_success_url(self):
        if '_save_and_update' in self.request.POST:
            return reverse(
                'sister_web_kelas_absensi_update',
                args=(self.object.id,)
            )
        return reverse(
            'sister_web_kelas_absensi_list',
            args=(self.object.kelas.id,)
        ) + "?semester=%s" % self.object.semester

    def get_initial(self):
        return {'kelas': self.object.kelas}

    def get_extra_context(self):
        extra_context = super().get_extra_context()
        PresensiSiswaFormSet = inlineformset_factory(
            PresensiKelas,
            PresensiSiswa,
            PresensiSiswaForm,
            fields=['siswa_kelas', 'status'],
            extra=0,
            can_delete=False
        )
        if self.request.POST:
            extra_context.update({
                'inline_fields': self.inline_fields,
                'inlineform': PresensiSiswaFormSet(
                    self.request.POST or None,
                    instance=self.object)
            })
        else:
            extra_context.update({
                'inline_fields': self.inline_fields,
                'inlineform': PresensiSiswaFormSet(
                    instance=self.object)
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


@website.register
class PresensiDelete(DeleteView):

    model = PresensiKelas
    url_name = 'kelas_absensi_delete'
    url_path = 'kelas_absensi/<str:object_id>/delete/'

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_absensi_list',
            args=(self.object.kelas.id,)
        ) + "?semester=%s" % self.object.semester

    def get_success_url(self):
        return reverse(
            'sister_web_kelas_absensi_list',
            args=(self.object.kelas.id,)
        ) + "?semester=%s" % self.object.semester

    def get_page_title(self):
        return "Konfirmasi"


@website.register
class RentangNilaiList(DetailView):
    model = Kelas
    url_path = 'kelas/<str:object_id>/rentang/'
    url_name = 'kelas_rentang_list'
    template_name = 'sister_web/pages/kelas_rentang.html'

    def get_backurl(self):
        return reverse('sister_web_kelas', args=(self.object.id,))

    def get_object_list(self, semester):
        # TODO cache
        return self.object.rentang_nilai.all()

    def get_extra_context(self):
        semester = self.request.GET.get('semester', 1)
        if int(semester) != 1:
            semester = 2
        extra_context = {
            'page_title': self.get_page_title(),
            'semester': int(semester),
            'object_list': self.get_object_list(int(semester))
        }
        return extra_context

    def get_page_title(self):
        return "%s %s" % ('Rentang Nilai', str(self.object))


@website.register
class RentangNilaiUpdate(UpdateView):

    model = RentangNilai
    form_class = RentangNilaiForm
    url_name = 'kelas_rentang_update'
    url_path = 'kelas_rentang/<str:object_id>/update/'

    def get_backurl(self):
        return reverse(
            'sister_web_kelas_rentang_list',
            args=(self.object.kelas.id,)
        )

    def get_success_url(self):
        return reverse(
            'sister_web_kelas_rentang_list',
            args=(self.object.kelas.id,)
        )

    def get_initial(self):
        return {'kelas': self.object.kelas}

    def get_page_title(self):
        return "Form Rentang"
