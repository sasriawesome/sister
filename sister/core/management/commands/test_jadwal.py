import pandas as pd
from django.db import models
from django.core.management import BaseCommand

class Command(BaseCommand):
    help = "Create sample kurikulum app datas"

    requires_migrations_checks = True
    requires_system_checks = True

    def handle(self, *args, **options):
        from django.apps import apps
        from django.db import transaction
        from django.conf import settings
        
        kelas_model = apps.get_model(
            'sister_pembelajaran.kelas', 
            require_ready=True
            )

        presensi_model = apps.get_model(
            'sister_pembelajaran.presensikelas', 
            require_ready=True
            )

        kelas = kelas_model.objects.first()

        results = presensi_model.objects.get_presensi_bulanan(
                kelas=kelas, semester=1, bulan=8
            ).prefetch_related('presensi_siswa')
        
        columns = ['id', 'siswa__nis', 'siswa__nisn', 'siswa__person__full_name']
        siswa_kelas_df = pd.DataFrame.from_records(kelas.siswa.values(*columns))
        siswa_kelas_df.set_index('id')
        print(siswa_kelas_df.index)
        
        for result in results:
            results_df = pd.DataFrame.from_records(result.presensi_siswa.values('siswa_kelas_id', 'status'))
            results_df.set_index('siswa_kelas_id')
            siswa_kelas_df.join(
                results_df,
                how='left'
            )
            print(siswa_kelas_df)