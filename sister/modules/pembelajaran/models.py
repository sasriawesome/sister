from django.db import models
from django.db.utils import cached_property
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone, translation
from django.core.validators import MinValueValidator, MaxValueValidator

from sister.core.models import BaseModel
from sister.core.enums import Weekday
from sister.modules.ruang.models import Ruang
from sister.modules.personal.models import Guru, Siswa
from sister.modules.kurikulum.models import (
    TahunAjaran,
    Kurikulum,
    MataPelajaran
)

from .managers import (
    KelasManager
)


__all__ = [
    'Kelas',
    'SiswaKelas',
    'MataPelajaranKelas',
    'RentangNilai',
    'JadwalPelajaran',
    'JadwalPiketSiswa',
    'KesehatanSiswa',
    'CatatanSiswa',
]

_ = translation.ugettext_lazy


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
    tahun_ajaran = models.ForeignKey(
        TahunAjaran,
        on_delete=models.CASCADE)
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
            raise ValidationError({
                'kurikulum': 'Kelas pada kurikulum tidak sesuai'
            })


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
        return "%s %s" % (self.kelas.nama_kelas, self.siswa)


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
    TINGKATKAN = 'tingkatkan'
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
        related_name='jadwal_pelajaran'
    )
    jam_mulai = models.TimeField(default=timezone.now)
    jam_berakhir = models.TimeField(default=timezone.now)
    deskripsi = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.mata_pelajaran)


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
        return "%s" % (self.siswa_kelas)


class KesehatanSiswa(BaseModel):
    class Meta:
        verbose_name = 'Kesehatan Siswa'
        verbose_name_plural = 'Kesehatan Siswa'
        unique_together = ('siswa_kelas', 'semester')

    siswa_kelas = models.ForeignKey(
        SiswaKelas,
        on_delete=models.CASCADE,
        related_name='kesehatan_siswa'
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

    def __str__(self):
        return "Kesehatan siswa %s Semester %s" % (
            self.siswa_kelas, self.semester)


class CatatanSiswa(BaseModel):
    class Meta:
        verbose_name = 'Catatan Siswa'
        verbose_name_plural = 'Catatan Siswa'
        unique_together = ('siswa_kelas', 'semester')

    siswa_kelas = models.ForeignKey(
        SiswaKelas,
        on_delete=models.CASCADE,
        related_name='catatan_siswa'
    )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    deskripsi = models.TextField()

    def __str__(self):
        return "Catatan siswa %s Semester %s" % (
            self.siswa_kelas, self.semester)


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
                nilai_minimum=81,
                nilai_maximum=100,
                aksi=RentangNilai.PERTAHANKAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='B',
                nilai_minimum=66,
                nilai_maximum=80,
                aksi=RentangNilai.TINGKATKAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='C',
                nilai_minimum=56,
                nilai_maximum=65,
                aksi=RentangNilai.TINGKATKAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='D',
                nilai_minimum=41,
                nilai_maximum=5,
                aksi=RentangNilai.PERLU_BIMBINGAN,
            )
        )
        rentang.append(
            RentangNilai(
                kelas=instance,
                predikat='E',
                nilai_minimum=0,
                nilai_maximum=40,
                aksi=RentangNilai.PERLU_BIMBINGAN,
            )
        )
        RentangNilai.objects.bulk_create(rentang)
