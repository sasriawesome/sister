import calendar
import pandas as pd
import numpy as np
from django.db import models
from django.utils import timezone


__all__ = [
    'KelasManager',
    'JadwalPelajaranManager'

]


class KelasManager(models.Manager):

    def get_siswa_kelas_df(self, kelas):
        siswa_kelas_df = pd.DataFrame(
            kelas.siswa.values('id', 'no_urut', 'siswa__person__full_name')
        )
        siswa_kelas_df = siswa_kelas_df.rename(
            columns={
                'no_urut': 'no',
                'siswa__person__full_name': 'nama_siswa'
            }
        )
        columns = ['id', 'no', 'nama_siswa']

        if not siswa_kelas_df.empty:
            siswa_kelas_df = siswa_kelas_df.set_index(columns)

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

    def get_matrix_presensi(self, kelas, semester, bulan):
        matrix = self.get_siswa_kelas_df(kelas)

        # Jika tidak ada siswa berhenti disini
        if matrix.empty:
            return matrix

        presensi_df = self.get_presensi_siswa_df(kelas, semester, bulan)
        days = calendar.monthrange(2020, bulan)[1]

        for day in range(1, days + 1):
            col_header = str(day).zfill(2)
            if not presensi_df.empty:
                result = presensi_df.loc[
                        pd.to_datetime(presensi_df['tanggal']).dt.day == day
                    ]
                result = result[['siswa_kelas_id', 'status']]
                result = result.rename(columns={'status': col_header})
                result = result.set_index('siswa_kelas_id')
            else:
                result = matrix.copy()
                result = result.reset_index(['no', 'nama_siswa'])
                result[col_header] = np.nan
                result = result[col_header]
            matrix = matrix.join(
                result,
                on='id',
                how='left'
            )

        matrix = matrix.replace({np.nan: None})
        matrix['H'] = matrix.eq('H').sum(axis=1)
        matrix['S'] = matrix.eq('S').sum(axis=1)
        matrix['I'] = matrix.eq('I').sum(axis=1)
        matrix['A'] = matrix.eq('A').sum(axis=1)
        matrix['L'] = matrix.eq('L').sum(axis=1)
        matrix = matrix.reset_index()
        matrix_index = ['id', 'no', 'nama_siswa', 'H', 'S', 'I', 'A', 'L']
        matrix = matrix.set_index(matrix_index)

        return matrix

    def get_rekap_presensi_siswa(self, kelas, semester, bulan):

        matrix = self.get_matrix_presensi(kelas, semester, bulan)

        summary = pd.DataFrame()
        summary['Hadir'] = matrix.eq('H').sum(axis=0)
        summary['Sakit'] = matrix.eq('S').sum(axis=0)
        summary['Izin'] = matrix.eq('I').sum(axis=0)
        summary['Tanpa Keterangan'] = matrix.eq('A').sum(axis=0)
        summary['Libur'] = matrix.eq('L').sum(axis=0)
        summary = summary.transpose()
        summary['total'] = summary.sum(axis=1)
        summary = summary.reset_index()
        summary_index = ['index', 'total']
        summary = summary.set_index(summary_index)

        return matrix, summary

    def get_rekap_presensi_siswa_dict(self, kelas, semester, bulan) -> dict:

        get_rekap = self.get_rekap_presensi_siswa
        matrix, summary = get_rekap(kelas, semester, bulan)
        matrix_presensi = matrix.transpose().to_dict()
        matrix_to_dict = []

        matrix_index = ['id', 'no', 'nama_siswa', 'H', 'S', 'I', 'A', 'L']
        for index, values in matrix_presensi.items():
            item = {}
            for idx in range(len(matrix_index)):
                item[matrix_index[idx]] = index[idx]
            item['matrix'] = values
            matrix_to_dict.append(item)

        summary = summary.transpose().to_dict()
        summary_index = ['index', 'total']
        summary_to_dict = []

        for index, values in summary.items():
            item = {}
            for idx in range(len(summary_index)):
                item[summary_index[idx]] = index[idx]
            item['matrix'] = values
            summary_to_dict.append(item)

        return {
            'header': matrix.columns,
            'results': matrix_to_dict,
            'summary': summary_to_dict
        }


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
                kelas=models.F('jadwal_kelas__kelas'),
                hari=models.F('jadwal_kelas__hari')
            )
