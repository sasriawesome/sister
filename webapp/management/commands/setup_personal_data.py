from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Create sample kurikulum app datas"

    requires_migrations_checks = True
    requires_system_checks = True

    def handle(self, *args, **options):
        from django.apps import apps
        from django.db import transaction
        """
        Perform:.
        1. Create Guru
        2. Create Wali
        3. Create Siswa
        """
        with transaction.atomic():
            # create super user
            person_model = apps.get_model(
                'sister_personal.person', require_ready=True)
            guru_model = apps.get_model(
                'sister_personal.guru', require_ready=True)
            wali_model = apps.get_model(
                'sister_personal.wali', require_ready=True)
            siswa_model = apps.get_model(
                'sister_personal.siswa', require_ready=True)

            # Create tahun ajaran
            print('Creating person ..')
            person1 = person_model(full_name='Sri Anisah', gender='P')
            person1.save()
            person2 = person_model(full_name='Rizki Sasri Dwitama', gender='L')
            person2.save()
            person3 = person_model(full_name='Mahathir Muhammad', gender='L')
            person3.save()
            person4 = person_model(
                full_name='Bacharudin Jusuf Habibie', gender='L')
            person4.save()
            person5 = person_model(full_name='M. Hafis', gender='L')
            person5.save()
            person6 = person_model(full_name='Ghallabi', gender='P')
            person6.save()

            print('Creating guru ..')
            guru1 = guru_model(person=person1, nip='111111')
            guru1.save()
            guru2 = guru_model(person=person2, nip='222222')
            guru2.save()

            print('Creating siswa ..')
            siswa1 = siswa_model(person=person4, nis='111', nisn='111')
            siswa1.save()
            siswa2 = siswa_model(person=person5, nis='222', nisn='222')
            siswa2.save()
            siswa3 = siswa_model(person=person6, nis='333', nisn='333')
            siswa3.save()

            print('Creating wali ..')
            wali1 = wali_model(siswa=siswa1, person=person1, status=2)
            wali1.save()
            wali2 = wali_model(siswa=siswa1, person=person2, status=1)
            wali2.save()
