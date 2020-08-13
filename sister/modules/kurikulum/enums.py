import enum


class AktifitasPendidikan(enum.Enum):

    AWAL_TAHUN_PELAJARAN = 1
    HARI_SEKOLAH_EFEKTIF = 2
    PENILAIAN_HARIAN = 3
    PENILAIAN_TENGAH_SEMESTER = 4
    PENILAIAN_AKHIR_SEMESTER = 5
    UJIAN_AKHIR_SEKOLAH = 6
    PENERIMAAN_RAPOR = 7
    HARI_MINGGU = 8
    HARI_LIBUR_UMUM = 9
    HARI_LIBUR_SEMESTER = 10
    HARI_LIBUR_PUASA = 11


HARI_LIBUR = (
    AktifitasPendidikan.HARI_MINGGU,
    AktifitasPendidikan.HARI_LIBUR_UMUM,
    AktifitasPendidikan.HARI_LIBUR_SEMESTER,
    AktifitasPendidikan.HARI_LIBUR_PUASA
)


AKTIFITAS_CHOICES = (
    (AktifitasPendidikan.AWAL_TAHUN_PELAJARAN.value,
        'Awal tahun pelajaran'),
    (AktifitasPendidikan.HARI_SEKOLAH_EFEKTIF.value,
        'Hari sekolah efektif'),
    (AktifitasPendidikan.PENILAIAN_HARIAN.value,
        'Penilaian harian'),
    (AktifitasPendidikan.PENILAIAN_TENGAH_SEMESTER.value,
        'Penilaian tengah semester'),
    (AktifitasPendidikan.PENILAIAN_AKHIR_SEMESTER.value,
        'Penilaian akhir semester'),
    (AktifitasPendidikan.UJIAN_AKHIR_SEKOLAH.value,
        'Ujian akhir sekolah'),
    (AktifitasPendidikan.PENERIMAAN_RAPOR.value,
        'Penerimaan rapor'),
    (AktifitasPendidikan.HARI_MINGGU.value,
        'Hari minggu'),
    (AktifitasPendidikan.HARI_LIBUR_UMUM.value,
        'Hari libur umum'),
    (AktifitasPendidikan.HARI_LIBUR_SEMESTER.value,
        'Hari libur semester'),
    (AktifitasPendidikan.HARI_LIBUR_PUASA.value,
        'Hari libur puasa')
)
