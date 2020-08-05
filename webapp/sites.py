from django.shortcuts import render


class WebApp:

    title = 'Website'
    description = 'Awesome Website'
    index_template_name = 'webapp/pages/index.html'

    def __init__(self, name='webapp'):
        self.name = name

    def get_urls(self):
        from django.urls import path
        return [
            path('', self.index_view, name='webapp_index'),
            path('kelas/', self.kelas_view, name='webapp_kelas'),
            path('mapel/', self.mapel_view, name='webapp_mapel'),
            path('profil/', self.profil_view, name='webapp_profil')
        ]

    def get_each_context(self, **kwargs):
        return {
            **kwargs,
            'web': self,
            'page_title': self.title
        }

    def index_view(self, request):
        context = self.get_each_context()
        context.update({})
        return render(request, self.index_template_name, context=context)

    def kelas_view(self, request):
        context = self.get_each_context()
        context.update({
            'object_list': [
                {
                    'nama': '1A 2020/2021',
                    'guru_kelas': 'Sri Anisah, S.Pd',
                    'tahun_ajaran': '2020/2021',
                    'jumlah_siswa': 30,
                    'get_status_display': 'Pending'
                }, {
                    'nama': '1B 2020/2021',
                    'guru_kelas': 'Sri Anisah, S.Pd',
                    'tahun_ajaran': '2020/2021',
                    'jumlah_siswa': 30,
                    'get_status_display': 'Aktif'

                }, {
                    'nama': '1C 2020/2021',
                    'guru_kelas': 'Sri Anisah, S.Pd',
                    'tahun_ajaran': '2019/2020',
                    'jumlah_siswa': 30,
                    'get_status_display': 'Selesai'
                }, {
                    'nama': '1D 2020/2021',
                    'guru_kelas': 'Sri Anisah, S.Pd',
                    'tahun_ajaran': '2019/2020',
                    'jumlah_siswa': 25,
                    'get_status_display': 'Selesai'
                },
            ]
        })
        return render(request, 'webapp/pages/kelas.html', context=context)

    def mapel_view(self, request):
        context = self.get_each_context()
        context.update({
            'object_list': [
                {
                    'nama': 'Pendidikan Pancasila dan Kewarganegaraan',
                    'tahun_ajaran': '2020/2021',
                    'guru': 'Sri Anisah, S.Pd',
                    'kelas': {
                        'nama': '1A 2020/2021',
                        'get_status_display': 'Selesai'
                    }
                }, {
                    'nama': 'Bahasa Indonesia',
                    'tahun_ajaran': '2020/2021',
                    'guru': 'Sri Anisah, S.Pd',
                    'kelas': {
                        'nama': '1A 2020/2021',
                        'get_status_display': 'Selesai'
                    }
                }, {
                    'nama': 'Pendidikan Pancasila dan Kewarganegaraan',
                    'tahun_ajaran': '2020/2021',
                    'guru': 'Sri Anisah, S.Pd',
                    'kelas': {
                        'nama': '1A 2020/2021',
                        'get_status_display': 'Selesai'
                    }
                }, {
                    'nama': 'Seni Budaya dan Prakarya',
                    'tahun_ajaran': '2020/2021',
                    'guru': 'Sri Anisah, S.Pd',
                    'kelas': {
                        'nama': '1A 2020/2021',
                        'get_status_display': 'Selesai'
                    }
                }
            ]
        })
        return render(request, 'webapp/pages/mapel.html', context=context)

    def profil_view(self, request):
        context = self.get_each_context()
        context.update({
            'instance': {
                    'nip': '123 322 123 332',
                    'person': {
                        'pid': '187107210041243',
                        'full_name': 'Sri Anisah S.Pd',
                        'short_name': 'Sri Anisah',
                        'title': 'Ibu',
                        'blood_type': 'O',
                        'get_gender_display': 'Perempuan',
                        'religion': 'Islam',
                        'date_of_birth': '24 Februari 1964',
                        'place_of_birth': 'Teluk Betung',
                        'job': 'PNS',
                        'income': 3000000,
                        'contact': {
                            'phone': '081366360114',
                            'whatsapp': '081366360114',
                            'email': 'sri.anisah@gmail.com',
                            'website': None,
                            'fax': None,
                        },
                        'address': {
                            'name': 'Rumah',
                            'street': 'Jl. Ikan Sebelah Gg. Flamboyan, No.8',
                            'city': 'Bandar Lampung',
                            'province': 'Lampung',
                            'country': 'Indonesia',
                            'zipcode': '35223'
                        }
                    },
                }
        })
        return render(request, 'webapp/pages/profil.html', context=context)

    def get_permission(self, request):
        """ """
        return request.user.is_authenticated


website = WebApp(name='webapp')
