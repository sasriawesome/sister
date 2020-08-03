import enum
import uuid
import decimal
from django.db import models
from django.db.utils import cached_property
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone, translation
from django.core.validators import MinValueValidator, MaxValueValidator

from polymorphic.models import PolymorphicModel

from sister.core.models import BaseModel
from sister.core.enums import Weekday
from sister.modules.ruang.models import Ruang
from sister.modules.personal.models import Guru, Siswa
from sister.modules.kurikulum.models import *

from .managers import *


__all__ = [
    'TahunAjaran',
    'Kelas',
    'SiswaKelas',
    'MataPelajaranKelas',
    'RentangNilai',
    'JadwalPelajaran',
    'JadwalPiketSiswa',
    'JadwalEkstraKurikuler',
    'PresensiKelas',
    'PresensiSiswa',
    'NilaiSiswa',
    'NilaiMataPelajaran',
    'NilaiMataPelajaranKTSP',
    'NilaiMataPelajaranK13',
]

_ = translation.ugettext_lazy


class TahunAjaran(BaseModel):
    class Meta:
        verbose_name = 'Tahun Ajaran'
        verbose_name_plural = 'Tahun Ajaran'

    BULAN = (
        (1, _('Januari')),
        (2, _('Februari')),
        (3, _('Maret')),
        (4, _('April')),
        (5, _('Mei')),
        (6, _('Juni')),
        (7, _('Juli')),
        (8, _('Agustus')),
        (9, _('September')),
        (10, _('Oktober')),
        (11, _('November')),
        (12, _('Desember')),
    )

    kode = models.CharField(
        max_length=10,
        editable=False, unique=True
    )
    tahun_mulai = models.IntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(3000),
        ]
    )
    bulan_mulai = models.IntegerField(
        choices=BULAN,
        default=7
    )
    tahun_akhir = models.IntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(3000),
        ]
    )
    bulan_akhir = models.IntegerField(
        choices=BULAN,
        default=6
    )

    def __str__(self):
        return self.kode

    def generate_kode(self):
        return "%s/%s" % (self.tahun_mulai, self.tahun_akhir)

    def save(self, *args, **kwargs):
        self.kode = self.generate_kode()
        super().save(*args, **kwargs)


class Kelas(BaseModel):
    class Meta:
        verbose_name = 'Kelas'
        verbose_name_plural = 'Kelas'
        ordering = ['kelas', 'tahun_ajaran__tahun_mulai']

    objects = KelasManager()

    nama_kelas = models.CharField(max_length=225)
    kelas = models.IntegerField(
        choices=[(x, x) for x in range(1, 13)],
        default=1
    )
    kurikulum = models.ForeignKey(
        Kurikulum, 
        on_delete=models.CASCADE,
        related_name='kelas_belajar')
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    guru_kelas = models.ForeignKey(
        Guru, 
        on_delete=models.CASCADE,
        related_name='kelas'
        )
    ruang = models.ForeignKey(
        Ruang, null=True, blank=False,
        on_delete=models.PROTECT,
        related_name='ruang')
    
    # Pengaturan Kelas
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1,
        help_text=_('Tampilkan informasi kelas berdasarkan semester')
    )
    status = models.CharField(
        max_length=10,
        choices=(
            ('PENDING', 'Pending'),
            ('AKTIF', 'Aktif'),
            ('SELESAI', 'Selesai'),
        ),
        default='PENDING',
        help_text=_('Tandai kelas sebagai: Pending, Aktif atau Selesai')
    )


    @cached_property
    def jumlah_siswa(self):
        return self.siswa.count()

    @cached_property
    def siswa_laki_laki(self):
        return self.siswa.filter(siswa__person__gender='L').count()

    @cached_property
    def siswa_perempuan(self):
        return self.siswa.filter(siswa__person__gender='P').count()
    
    @cached_property
    def jadwal_pelajaran_semester(self):
        return self.jadwal_pelajaran.filter(semester=self.semester)

    @cached_property
    def piket_semester(self):
        return self.piket.filter(semester=self.semester)

    @cached_property
    def presensi_semester(self):
        return self.presendi.filter(semester=self.semester)

    def __str__(self):
        return "%s %s" % (self.nama_kelas, self.tahun_ajaran)

    def clean(self):
        if not getattr(self, 'kurikulum', False):
            raise ValidationError({'kurikulum': 'silahkan pilih kurikulum'})

        if self.kurikulum.kelas != self.kelas:
            raise ValidationError({'kurikulum': 'Kelas pada kurikulum tidak sesuai'})


class SiswaKelas(BaseModel):
    class Meta:
        verbose_name = 'Siswa Kelas'
        verbose_name_plural = 'Siswa Kelas'
        ordering = ['no_urut']
        unique_together = ('siswa', 'kelas')

    kelas = models.ForeignKey(
        Kelas, related_name='siswa',
        on_delete=models.CASCADE
        )
    no_urut = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    siswa = models.ForeignKey(
        Siswa,
        related_name='kelas',
        on_delete=models.CASCADE
        )
    status = models.IntegerField(
        choices=(
            (1, 'Baru'),
            (2, 'Tinggal Kelas'),
            (99, 'Lainnya'),
        ),
        default=1
    )
    status_lain = models.CharField(max_length=56, null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.kelas, self.siswa)


class RentangNilai(BaseModel):
    class Meta:
        verbose_name = 'Rentang Nilai'
        verbose_name_plural = 'Rentang Nilai'
        unique_together = ('kelas', 'predikat')

    PREDIKAT = (
        ('A', 'sangat baik'),
        ('B', 'baik'),
        ('C', 'cukup baik'),
        ('D', 'kurang baik'),
        ('E', 'sangat kurang'),
    )

    PERTAHANKAN = 'pertahankan' 
    TINGKATKAN =  'tingkatkan'
    PERLU_BIMBINGAN = 'perlu_bimbingan'

    AKSI = (
        (PERTAHANKAN, 'pertahankan'),
        (TINGKATKAN, 'tingkatkan'),
        (PERLU_BIMBINGAN, 'perlu bimbingan'),
    )

    kelas = models.ForeignKey(
        Kelas, on_delete=models.CASCADE,
        related_name='rentang_nilai'
        )
    nilai_minimum = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    nilai_maximum = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    predikat = models.CharField(
        max_length=1,
        choices=PREDIKAT,
        default='A'
    )
    aksi = models.CharField(
        max_length=125,
        choices=AKSI,
        default=TINGKATKAN
    )

    def __str__(self):
        return self.predikat


class MataPelajaranKelas(BaseModel):
    class Meta:
        verbose_name = 'Guru Mata Pelajaran'
        verbose_name_plural = 'Guru Mata Pelajaran'
        unique_together = ('kelas', 'mata_pelajaran')

    kelas = models.ForeignKey(
        Kelas,
        on_delete=models.CASCADE,
        related_name='mata_pelajaran_kelas')
    mata_pelajaran = models.ForeignKey(
        MataPelajaran,
        on_delete=models.CASCADE,
        related_name='mata_pelajaran_kelas'
    )
    guru = models.ForeignKey(
        Guru,
        on_delete=models.CASCADE,
        related_name='mata_pelajaran_kelas'
        )
    kkm = models.PositiveIntegerField(
        default=65,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Kriteria Ketuntasan Minimal'
    )
    tugas = models.PositiveIntegerField(
        default=10,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Tugas dan Pekerjaan Rumah'
    )
    ph = models.PositiveIntegerField(
        default=20,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Penilaian Harian'
    )
    pts = models.PositiveIntegerField(
        default=30,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Penilaian Tengah Semester'
    )
    pas = models.PositiveIntegerField(
        default=40,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        help_text='Penilaian Akhir Semester'
    )

    @property
    def total(self):
        total_bobot = (
            self.tugas 
            + self.ph 
            + self.pts 
            + self.pas)
        return total_bobot

    def __str__(self):
        return "%s %s" % (self.kelas, self.mata_pelajaran)


class JadwalPelajaran(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Kelas'
        verbose_name_plural = 'Jadwal Kelas'
        unique_together = ('kelas', 'semester', 'hari', 'mata_pelajaran')

    kelas = models.ForeignKey(
        Kelas, on_delete=models.CASCADE,
        related_name='jadwal_pelajaran')
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    hari = models.IntegerField(
        choices=Weekday.CHOICES.value,
        default=Weekday.MONDAY.value
    )
    mata_pelajaran = models.ForeignKey(
        MataPelajaranKelas,
        on_delete=models.CASCADE,
        null=True, blank=True, # TODO should not null
        related_name='jadwal_pelajaran'
    )
    jam_mulai = models.TimeField(default=timezone.now)
    jam_berakhir = models.TimeField(default=timezone.now)
    deskripsi = models.CharField(max_length=225, null=True, blank=True)
    
    def __str__(self):
        return "%s %s" % (self.kelas, self.get_hari_display())


class JadwalPiketSiswa(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Piket Siswa'
        verbose_name_plural = 'Jadwal Piket Siswa'
        unique_together = ('kelas', 'semester', 'hari', 'siswa_kelas')

    kelas = models.ForeignKey(
        Kelas, on_delete=models.CASCADE,
        related_name='piket')
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    hari = models.IntegerField(
        choices=Weekday.CHOICES.value,
        default=Weekday.MONDAY.value
    )
    siswa_kelas = models.ForeignKey(
        SiswaKelas, 
        null=True, blank=True,
        related_name='piket_kelas',
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.kelas, self.get_hari_display())


class JadwalEkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Ekstra Kurikuler'
        verbose_name_plural = 'Jadwal Ekstra Kurikuler'
        unique_together = ('hari', 'semester', 'kelas', 'ekstra_kurikuler')


    kelas = models.ForeignKey(
        Kelas,
        on_delete=models.CASCADE,
        related_name='jadwal_ekskul'
        )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    hari = models.IntegerField(
        choices=Weekday.CHOICES.value,
        default=Weekday.MONDAY.value
    )
    ekstra_kurikuler = models.ForeignKey(
        EkstraKurikuler,
        on_delete=models.CASCADE,
        related_name='jadwal'
    )
    jam_mulai = models.TimeField(default=timezone.now)
    jam_berakhir = models.TimeField(default=timezone.now)
    deskripsi = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return "%s" % self.ekstra_kurikuler


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

    LIBUR = (
        HARI_MINGGU,
        HARI_LIBUR_UMUM,
        HARI_LIBUR_SEMESTER,
        HARI_LIBUR_PUASA
    )

    CHOICES = (
        (AWAL_TAHUN_PELAJARAN, 'Awal tahun pelajaran'),
        (HARI_SEKOLAH_EFEKTIF, 'Hari sekolah efektif'),
        (PENILAIAN_HARIAN, 'Penilaian harian'),
        (PENILAIAN_TENGAH_SEMESTER, 'Penilaian tengah semester'),
        (PENILAIAN_AKHIR_SEMESTER, 'Penilaian akhir semester'),
        (UJIAN_AKHIR_SEKOLAH, 'Ujian akhir sekolah'),
        (PENERIMAAN_RAPOR, 'Penerimaan rapor'),
        (HARI_MINGGU, 'Hari minggu'),
        (HARI_LIBUR_UMUM, 'Hari minggu'),
        (HARI_LIBUR_SEMESTER, 'Hari libur semester'),
        (HARI_LIBUR_PUASA, 'Hari libur semester')
    )

class PresensiKelas(BaseModel):
    class Meta:
        verbose_name = 'Presensi Kelas'
        verbose_name_plural = 'Presensi Kelas'
        ordering = ['-tanggal']
        unique_together = ('kelas', 'tanggal')

    objects = PresensiKelasManager()

    kelas = models.ForeignKey(
        Kelas, on_delete=models.CASCADE,
        related_name='presensi'
        )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
        )
    tanggal = models.DateField(default=timezone.now)
    aktifitas = models.IntegerField(
        choices=AktifitasPendidikan.CHOICES.value,
        default=AktifitasPendidikan.HARI_SEKOLAH_EFEKTIF.value,
        help_text=_('Alasan kelas diliburkan, atau catatan lain.')
        )
    deskripsi = models.CharField(
        max_length=250,
        null=True, blank=True,
        help_text=_('Penjelasan aktifitas.')
        )
        
    @cached_property
    def hari(self):
        return Weekday.CHOICES.value[self.tanggal.weekday()][1]

    @cached_property
    def hadir(self):
        return self.presensi_siswa.filter(status='H').count()

    @cached_property
    def sakit(self):
        return self.presensi_siswa.filter(status='S').count()

    @cached_property
    def izin(self):
        return self.presensi_siswa.filter(status='I').count()

    @cached_property
    def tanpa_keterangan(self):
        return self.presensi_siswa.filter(status='A').count()

    @cached_property
    def total(self):
        return self.presensi_siswa.count()

    def __str__(self):
        return "%s %s" % (self.kelas, self.tanggal)


class PresensiSiswa(BaseModel):
    class Meta:
        verbose_name = 'Presensi Siswa'
        verbose_name_plural = 'Presensi Siswa'
        unique_together = ('presensi_kelas', 'siswa_kelas')

    objects = PresensiSiswaManager()

    presensi_kelas = models.ForeignKey(
        PresensiKelas,
        on_delete=models.CASCADE,
        related_name='presensi_siswa'
    )
    siswa_kelas = models.ForeignKey(
        SiswaKelas,
        on_delete=models.CASCADE,
        related_name='presensi'
    )
    status = models.CharField(
        max_length=3,
        choices=(
            ('H', 'Hadir'),
            ('S', 'Sakit'),
            ('I', 'Izin'),
            ('A', 'Tanpa Keterangan'),
        ),
        default='H'
    )

    def __str__(self):
        return "%s %s" % (self.presensi_kelas, self.siswa_kelas)


class NilaiSiswa(BaseModel):
    class Meta:
        verbose_name = 'Nilai Siswa'
        verbose_name_plural = 'Nilai Siswa'
        unique_together = ('siswa', 'semester')
        
    siswa = models.ForeignKey(
        SiswaKelas, 
        on_delete=models.CASCADE,
        related_name='nilai_siswa'
    )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    
    berat_badan = models.IntegerField(
        default=15,
        validators=[
            MinValueValidator(15),
            MaxValueValidator(100)
        ]
    )
    tinggi_badan = models.IntegerField(
        default=50,
        validators=[
            MinValueValidator(50),
            MaxValueValidator(200)
        ]
    )

    nilai_spiritual = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    predikat_spiritual = models.CharField(max_length=1, null=True, blank=True)
    deskripsi_spiritual = models.TextField(null=True, blank=True)
    
    nilai_sosial = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    predikat_sosial = models.CharField(max_length=1, null=True, blank=True)
    deskripsi_sosial = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Nilai siswa %s Semester %s" % (self.siswa, self.semester)


class NilaiMataPelajaran(PolymorphicModel, BaseModel):
    class Meta:
        verbose_name = 'Nilai Mata Pelajaran'
        verbose_name_plural = 'Nilai Pelajaran'
        unique_together = ('nilai_siswa', 'mata_pelajaran')
    
    no_urut = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    nilai_siswa = models.ForeignKey(
        NilaiSiswa, 
        on_delete=models.CASCADE,
        related_name='nilai_mata_pelajaran'
    )
    mata_pelajaran = models.ForeignKey(
        MataPelajaran,
        on_delete=models.CASCADE,
        related_name='nilai_siswa'
    )
    kkm = models.IntegerField(
        default=65,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )


class NilaiMataPelajaranKTSP(NilaiMataPelajaran):
    class Meta:
        verbose_name = 'Nilai Mata Pelajaran KTSP'
        verbose_name_plural = 'Nilai Mata Pelajaran KTSP'

    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    deskripsi = models.TextField()


class NilaiMataPelajaranK13(NilaiMataPelajaran):
    class Meta:
        verbose_name = 'Nilai Mata Pelajaran K13'
        verbose_name_plural = 'Nilai Mata Pelajaran K13'
    nilai_pengetahuan = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    predikat_pengetahuan = models.CharField(max_length=1, null=True, blank=True)
    deskripsi_pengetahuan = models.TextField(null=True, blank=True)
    
    nilai_keterampilan = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ])
    predikat_keterampilan = models.CharField(max_length=1, null=True, blank=True)
    deskripsi_keterampilan = models.TextField(null=True, blank=True)



@receiver(post_save, sender=Kelas)
def after_save_kelas(sender, **kwargs):
    created = kwargs.pop('created', None)
    instance = kwargs.pop('instance', None)
    if created:
        # create rentang nilai kosong
        rentang = []
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='A',
                nilai_minimum = 81,
                nilai_maximum = 100,
                aksi = RentangNilai.PERTAHANKAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='B',
                nilai_minimum = 66,
                nilai_maximum = 80,
                aksi = RentangNilai.TINGKATKAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='C',
                nilai_minimum = 56,
                nilai_maximum = 65,
                aksi = RentangNilai.TINGKATKAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='D',
                nilai_minimum = 41,
                nilai_maximum = 55,
                aksi = RentangNilai.PERLU_BIMBINGAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='E',
                nilai_minimum = 0,
                nilai_maximum = 40,
                aksi = RentangNilai.PERLU_BIMBINGAN,
            )
        )
        RentangNilai.objects.bulk_create(rentang)


@receiver(post_save, sender=PresensiKelas)
def after_save_presensi_siswa(sender, **kwargs):
    created = kwargs.pop('created', None)
    instance = kwargs.pop('instance', None)
    if created:
        # add initial items
        items = []
        for siswa in instance.kelas.siswa.all():
            items.append(
                PresensiSiswa(
                    siswa_kelas=siswa,
                    presensi_kelas=instance
                )
            )
        PresensiSiswa.objects.bulk_create(items)