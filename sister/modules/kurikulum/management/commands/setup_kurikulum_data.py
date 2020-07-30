from django.core.management import BaseCommand

class Command(BaseCommand):
    help = "Create sample kurikulum app datas"

    requires_migrations_checks = True
    requires_system_checks = True

    def handle(self, *args, **options):
        from django.apps import apps
        from django.db import transaction
        from django.conf import settings
        """
        Perform:.
        1. Create Tahun Ajaran
        2. Create Kurikulum
        3. Create Mata Pelajaran
        4. Add Mata Pelajaran Kurikulum
        5. Create ExtraKurikuler
        """
        with transaction.atomic():
            # create super user
            user_model = apps.get_model(settings.AUTH_USER_MODEL, require_ready=True)
            superuser = user_model.objects.create_superuser(
                username='rizki_sasri',
                password='habibie099',
                email='sasri.gg@gmail.com'
                )

            # Create tahun ajaran
            print('Creating tahun ajaran ..')
            ta_model = apps.get_model('sister_pembelajaran.tahunajaran', require_ready=True)
            ta1 = ta_model(
                tahun_mulai = 2020,
                tahun_akhir = 2021
            )
            ta1.save()
            print('Tahun ajaran %s created..' % ta1)

            ta2 = ta_model(
                tahun_mulai = 2021,
                tahun_akhir = 2022
            )
            ta2.save()
            print('Tahun ajaran %s created..' % ta2)

            # Create kurikulum
            kurikulum_model = apps.get_model('sister_kurikulum.kurikulum', require_ready=True)
            print('Creating kurikulum ..')
            krk1 = kurikulum_model(
                nama='Kurikulum K13 SD Kelas 1 Revisi 2018',
                tahun=2013,
                tingkat=1,
                kelas=1,
                revisi=2018
            )
            krk1.save()
            print('Kurikulum %s created..' % krk1)

            krk2 = kurikulum_model(
                nama='Kurikulum K13 SD Kelas 2 Revisi 2018',
                tahun=2013,
                tingkat=1,
                kelas=2,
                revisi=2018
            )
            krk2.save()
            print('Kurikulum %s created..' % krk2)
            
            krk3 = kurikulum_model(
                nama='Kurikulum K13 SD Kelas 3 Revisi 2018',
                tahun=2013,
                tingkat=1,
                kelas=3,
                revisi=2018
            )
            krk3.save()
            print('Kurikulum %s created..' % krk3)

            krk4 = kurikulum_model(
                nama='Kurikulum K13 SD Kelas 4 Revisi 2018',
                tahun=2013,
                tingkat=1,
                kelas=4,
                revisi=2018
            )
            krk4.save()
            print('Kurikulum %s created..' % krk4)

            krk5 = kurikulum_model(
                nama='Kurikulum K13 SD Kelas 5 Revisi 2018',
                tahun=2013,
                tingkat=1,
                kelas=5,
                revisi=2018
            )
            krk5.save()
            print('Kurikulum %s created..' % krk5)

            krk6 = kurikulum_model(
                nama='Kurikulum K13 SD Kelas 6 Revisi 2018',
                tahun=2013,
                tingkat=1,
                kelas=6,
                revisi=2018
            )
            krk6.save()
            print('Kurikulum %s created..' % krk6)

            krk7 = kurikulum_model(
                nama='Kurikulum K13 SMP Kelas 1 Revisi 2018',
                tahun=2013,
                tingkat=2,
                kelas=7,
                revisi=2018
            )
            krk7.save()
            print('Kurikulum %s created..' % krk7)

            # Create Mata Pelajaran
            print('Creating mata pelajaran ..')
            mapel_model = apps.get_model('sister_kurikulum.matapelajaran', require_ready=True)

            pai = mapel_model(kode='PAI', nama='Pendidikan Agama Islam')
            pai.save()
            
            pab = mapel_model(kode='PAB', nama='Pendidikan Agama Budha')
            pab.save()
            
            pap = mapel_model(kode='PAP', nama='Pendidikan Agama Protestan')
            pap.save()
            
            pak = mapel_model(kode='PAK', nama='Pendidikan Agama Katolik')
            pak.save()
            
            pac = mapel_model(kode='PAC', nama='Pendidikan Agama Khonghucu')
            pac.save()
            
            pah=mapel_model(kode='PAH', nama='Pendidikan Agama Hindu')
            pah.save()
            
            ppkn = mapel_model(kode='PPKn', nama='Pendidikan Pancasila dan Kewarganegaraan')
            ppkn.save()
            
            bind = mapel_model(kode='BIND', nama='Bahasa Indonesia')
            bind.save()
            
            bing = mapel_model(kode='BING', nama='Bahasa Inggris')
            bing.save()

            sbdp = mapel_model(kode='SBdP', nama='Seni Budaya dan Keterampilan')
            sbdp.save()

            pjok = mapel_model(kode='PJOK', nama='Pendidikan Jasmani dan Olah Raga')
            pjok.save()

            ipa = mapel_model(kode='IPA', nama='Ilmu Pengetahuan Alam')
            ipa.save()

            ips = mapel_model(kode='IPS', nama='Ilmu Pengetahuan Sosial')
            ips.save()

            mtk = mapel_model(kode='MTK', nama='Matematika')
            mtk.save()

            tik = mapel_model(kode='TIK', nama='Teknologi Informasi dan Komputer')
            tik.save()
            
            print('Mata pelajaran created..')

            # Add Mata Pelajaran to Kurikulum
            mpkrk_model = apps.get_model('sister_kurikulum.matapelajarankurikulum', require_ready=True)
            print('Adding mata pelajaran to kurikulum ..')
            print('Adding mata pelajaran to kurikulum %s..' % krk1)
            krk1_pai = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=pai)
            krk1_pab = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=pab)
            krk1_pap = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=pap)
            krk1_pak = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=pak)
            krk1_pac = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=pac)
            krk1_pah = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=pah)
            krk1_bind = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=bind)
            krk1_ppkn = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=ppkn)
            krk1_mtk = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=mtk)
            krk1_sbdp = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=sbdp)
            krk1_pjok = mpkrk_model.objects.create(kurikulum=krk1, mata_pelajaran=pjok)

            print('Adding mata pelajaran to kurikulum %s..' % krk2)
            krk2_pai = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=pai)
            krk2_pab = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=pab)
            krk2_pap = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=pap)
            krk2_pak = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=pak)
            krk2_pac = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=pac)
            krk2_pah = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=pah)
            krk2_bind = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=bind)
            krk2_ppkn = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=ppkn)
            krk2_mtk = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=mtk)
            krk2_sbdp = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=sbdp)
            krk2_pjok = mpkrk_model.objects.create(kurikulum=krk2, mata_pelajaran=pjok)
            print("Mata pelajaran kurikulum added")
