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