from django.shortcuts import render, reverse

mapel_list = [
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

jadwal_list = [
        {
            'id': 1,
            'nama': '1A 2020/2021',
            'guru_kelas': 'Sri Anisah, S.Pd',
            'tahun_ajaran': '2020/2021',
            'jumlah_siswa': 30,
            'get_status_display': 'Pending'
        }, {
            'id': 2,
            'nama': '1B 2020/2021',
            'guru_kelas': 'Sri Anisah, S.Pd',
            'tahun_ajaran': '2020/2021',
            'jumlah_siswa': 30,
            'get_status_display': 'Aktif'

        }, {
            'id': 3,
            'nama': '1C 2020/2021',
            'guru_kelas': 'Sri Anisah, S.Pd',
            'tahun_ajaran': '2019/2020',
            'jumlah_siswa': 30,
            'get_status_display': 'Selesai'
        }, {
            'id': 4,
            'nama': '1D 2020/2021',
            'guru_kelas': 'Sri Anisah, S.Pd',
            'tahun_ajaran': '2019/2020',
            'jumlah_siswa': 25,
            'get_status_display': 'Selesai'
        },
    ]

piket_list = [
        {
            'kelas': '1A 2020/2021',
            'semester': 1,
            'hari': 0,
            'siswa_kelas': 'Bacharuddin Jusuf Habibie',
        }, {
            'kelas': '1A 2020/2021',
            'semester': 1,
            'hari': 0,
            'siswa_kelas': 'Mahathir Muhammad',
        }, {
            'kelas': '1A 2020/2021',
            'semester': 1,
            'hari': 1,
            'siswa_kelas': 'Bacharuddin Jusuf Habibie',
        }, {
            'kelas': '1A 2020/2021',
            'semester': 1,
            'hari': 1,
            'siswa_kelas': 'Mahathir Muhammad',
        }
    ]


kelas_list = [
        {
            'id': 1,
            'nama': '1A 2020/2021',
            'guru_kelas': 'Sri Anisah, S.Pd',
            'tahun_ajaran': '2020/2021',
            'jumlah_siswa': 30,
            'get_status_display': 'Pending'
        }, {
            'id': 2,
            'nama': '1B 2020/2021',
            'guru_kelas': 'Sri Anisah, S.Pd',
            'tahun_ajaran': '2020/2021',
            'jumlah_siswa': 30,
            'get_status_display': 'Aktif'

        }, {
            'id': 3,
            'nama': '1C 2020/2021',
            'guru_kelas': 'Sri Anisah, S.Pd',
            'tahun_ajaran': '2019/2020',
            'jumlah_siswa': 30,
            'get_status_display': 'Selesai'
        }, {
            'id': 4,
            'nama': '1D 2020/2021',
            'guru_kelas': 'Sri Anisah, S.Pd',
            'tahun_ajaran': '2019/2020',
            'jumlah_siswa': 25,
            'get_status_display': 'Selesai'
        },
    ]

kelas_instance = {
        'id': 1,
        'nama': '1A 2020/2021',
        'guru_kelas': {
            'person': 'Sri Anisah, S.Pd',
            'nip': '1231231212312',
        },
        'tahun_ajaran': '2020/2021',
        'jumlah_siswa': 30,
        'kurikulum': 'K13.T1.K1.R2018',
        'get_status_display': 'Pending',
        'ruang': '1A',
        'mata_pelajaran': [
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
        ],
        'siswa': [
            {
                'id': 1,
                'no_urut': 1,
                'siswa': {
                    'nis': 111111,
                    'nisn': 333333,
                    'person': {
                        'full_name': 'Bacharuddin Jusuf Habibie',
                    }
                }
            }, {
                'id': 2,
                'no_urut': 2,
                'siswa': {
                    'nis': 22222,
                    'nisn': 333333,
                    'person': {
                        'full_name': 'Bacharuddin Jusuf Habibie',
                    }
                }
            }, {
                'id': 3,
                'no_urut': 3,
                'siswa': {
                    'nis': 333333,
                    'nisn': 333333,
                    'person': {
                        'full_name': 'Bacharuddin Jusuf Habibie',
                    }
                }
            }, {
                'id': 4,
                'no_urut': 4,
                'siswa': {
                    'nis': 444444,
                    'nisn': 333333,
                    'person': {
                        'full_name': 'Bacharuddin Jusuf Habibie',
                    }
                }
            }, {
                'id': 5,
                'no_urut': 5,
                'siswa': {
                    'nis': 555555,
                    'nisn': 333333,
                    'person': {
                        'full_name': 'Bacharuddin Jusuf Habibie',
                        }
                    }
            }, {
                'id': 6,
                'no_urut': 6,
                'siswa': {
                    'nis': 666666,
                    'nisn': 333333,
                    'person': {
                        'full_name': 'Bacharuddin Jusuf Habibie',
                        }
                    }
                }

        ]
    }

guru_instance = {
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
            path('search/', self.kelas_view, name='webapp_search'),
            path('profil/', self.profil_view, name='webapp_profil'),
            path(
                'kelas/<str:object_id>/',
                self.kelas_view,
                name='webapp_kelas'
                ),
            # path(
            #     'kelas_jadwal/<str:object_id>/',
            #     self.kelas_jadwal_view,
            #     name='webapp_kelas_jadwal'
            #     ),
            # path(
            #     'kelas_piket/<str:object_id>/',
            #     self.kelas_piket_view,
            #     name='webapp_kelas_piket'
            #     ),
            path('mapel/', self.mapel_view, name='webapp_mapel'),
        ]

    def get_each_context(self, **kwargs):
        return {
            **kwargs,
            'web': self,
            'page_title': self.title
        }

    def index_view(self, request):
        context = self.get_each_context()
        context.update({
            'kelas': kelas_list,
            'mapel': mapel_list
        })
        return render(request, self.index_template_name, context=context)

    # def search_kelas_view(self, request):
    #     context = self.get_each_context()
    #     context.update({
    #         'backurl': reverse('webapp_index'),
    #         'page_title': 'Cari Kelas',
    #         'object_list': kelas_list
    #     })
    #     return render(
    #         request, 'webapp/pages/search_kelas.html', context=context)

    def kelas_view(self, request, object_id):
        context = self.get_each_context()
        page_mode = request.GET.get('page_mode', None)
        context.update({
            'page_mode': page_mode,
            'backurl': reverse('webapp_index'),
            'page_title': kelas_instance['nama'],
            'instance': kelas_instance
            })
        return render(
            request, 'webapp/pages/kelas.html', context=context)

    # def kelas_jadwal_view(self, request, object_id):
    #     context = self.get_each_context()
    #     context.update({
    #         'backurl': reverse('webapp_kelas', args=(1,)),
    #         'page_title': 'Jadwal Pelajaran',
    #         'instance': kelas_instance,
    #         'object_list': jadwal_list
    #     })
    #     return render(
    #         request, 'webapp/pages/jadwal.html', context=context)

    # def kelas_piket_view(self, request, object_id):
    #     context = self.get_each_context()
    #     context.update({
    #         'backurl': reverse('webapp_kelas', args=(1,)),
    #         'page_title': 'Jadwal Piket Kelas',
    #         'instance': kelas_instance,
    #         'object_list': piket_list
    #     })
    #     return render(
    #         request, 'webapp/pages/piket.html', context=context)

    def mapel_view(self, request):
        context = self.get_each_context()
        context.update({
            'object_list': mapel_list
        })
        return render(request, 'webapp/pages/mapel.html', context=context)

    def profil_view(self, request):
        context = self.get_each_context()
        context.update({
            'backurl': reverse('webapp_index'),
            'page_title': 'Profil Saya',
            'instance': guru_instance
        })
        return render(request, 'webapp/pages/profil.html', context=context)

    def get_permission(self, request):
        """ """
        return request.user.is_authenticated


website = WebApp(name='webapp')
