import enum


def snake_to_lower(text):
    return text.replace('_', ' ').lower()


class JenisKurikulum(enum.Enum):
    KTSP = 1
    K13 = 2


class KompetensiInti(enum.Enum):
    SIKAP_SPIRITUAL = 1
    SIKAP_SOSIAL = 2
    PENGETAHUAN = 3
    KETERAMPILAN = 4


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


SEMESTER_CHOICES = ((1, 1), (2, 2),)
JENIS_KURIKULUM_CHOICES = (
    (x.value, snake_to_lower(x.name).title()) for x in JenisKurikulum)
KOMPETENSI_INTI_CHOICES = (
    (x.value, snake_to_lower(x.name).title()) for x in KompetensiInti)

HARI_LIBUR = (
    AktifitasPendidikan.HARI_MINGGU.value,
    AktifitasPendidikan.HARI_LIBUR_UMUM.value,
    AktifitasPendidikan.HARI_LIBUR_SEMESTER.value,
    AktifitasPendidikan.HARI_LIBUR_PUASA.value
)

AKTIFITAS_CHOICES = (
    (x.value, snake_to_lower(x.name).title()) for x in AktifitasPendidikan
    )
