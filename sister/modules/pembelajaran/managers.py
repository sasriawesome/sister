import calendar
import pandas as pd
import numpy as np
from django.db import models

__all__ = [
    'KelasManager',
    'PresensiKelasManager',
    'PresensiSiswaManager',
    'JadwalPelajaranManager',
    'JadwalEkskulManager'

]


class KelasManager(models.Manager):

    def get_siswa_kelas_df(self, kelas):
        siswa_kelas_df = pd.DataFrame(
            kelas.siswa.values('id', 'no_urut','siswa__person__full_name')
        )
        siswa_kelas_df['index'] = siswa_kelas_df['id']
        siswa_kelas_df = siswa_kelas_df.set_index('index')    
        siswa_kelas_df = siswa_kelas_df.rename(
            columns={
                'siswa__no_urut':'no',
                'siswa__person__full_name':'full_name'
            }
        )

        return siswa_kelas_df
    
    def get_presensi_siswa_df(self, kelas, semester, bulan):
        from sister.modules.pembelajaran.models import PresensiSiswa
        presensi = PresensiSiswa.objects.filter(
            presensi_kelas__kelas=kelas,
            presensi_kelas__semester=semester,
            presensi_kelas__tanggal__month=bulan
        ).annotate(
            tanggal=models.F('presensi_kelas__tanggal'),
            semester=models.F('presensi_kelas__semester'),
        ).values(
            'siswa_kelas_id', 'status', 'tanggal', 'semester'
        )

        presensi_df = pd.DataFrame(presensi)
        return presensi_df
        
    def get_rekap_presensi(self, kelas, semester, bulan):
        
        results_df = self.get_siswa_kelas_df(kelas)
        presensi_df = self.get_presensi_siswa_df(kelas, semester, bulan)

        days = calendar.monthrange(2020, bulan)[1]

        for day in range(1, days + 1):

            if not presensi_df.empty:
                result = presensi_df.loc[pd.to_datetime(presensi_df['tanggal']).dt.day == day]
                result = result[['siswa_kelas_id', 'status']]
                result = result.rename(columns={'status': day})
                result = result.set_index('siswa_kelas_id')
            else:
                result = results_df.copy()
                result[day] = np.nan
                result = result[day]

            results_df = results_df.join(
                result,
                on='id',
                how='left'
            )

        results_df = results_df.replace({np.nan: None})
        results_df['H'] = results_df.eq('H').sum(axis=1)
        results_df['S'] = results_df.eq('S').sum(axis=1)
        results_df['I'] = results_df.eq('I').sum(axis=1)
        results_df['A'] = results_df.eq('A').sum(axis=1)
        results_df['L'] = results_df.eq('L').sum(axis=1)
        return results_df


class PresensiKelasManager(models.Manager):
    pass


class PresensiSiswaManager(models.Manager):
    pass


class JadwalPelajaranManager(models.Manager):
    pass


class ItemJadwalPelajaran(models.Manager):
    def get_by_kelas(self, kelas, current_day=True):
        filters = {
                'kelas': kelas.id,
            }
        if current_day:
            filters['hari'] = timezone.now().weekday()
        return self.filter(**filters).annotate(
                kelas = models.F('jadwal_kelas__kelas'),
                hari = models.F('jadwal_kelas__hari')
            )


class JadwalEkskulManager(models.Manager):
    pass

    def get_by_kelas(self, kelas, current_day=True):
        filters = {
                'jadwal_kelas__kelas': kelas.id,
            }
        if current_day:
            filters['hari'] = timezone.now().weekday()
        return self.filter(**filters).annotate(
                kelas = models.F('jadwal_kelas__kelas'),
                hari = models.F('jadwal_kelas__hari')
            )