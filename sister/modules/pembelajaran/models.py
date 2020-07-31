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
from sister.modules.ruang.models import Ruang
from sister.modules.personal.models import Guru, Siswa
from sister.modules.kurikulum.models import (
    Kurikulum, MataPelajaran, MataPelajaranKurikulum, EkstraKurikuler
    )

__all__ = [
    'TahunAjaran',
    'Kelas',
    'SiswaKelas',
    'MataPelajaranKelas',
    'RentangNilai',
    'JadwalKelas',
    'ItemJadwalPelajaran',
    'ItemJadwalEkstraKurikuler',
    'PresensiKelas',
    'PresensiSiswa',
    'PiketKelas',
    'ItemPiketKelas',
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
    tahun_akhir = models.IntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(3000),
        ]
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
    status = models.CharField(
        max_length=10,
        choices=(
            ('PENDING', 'Pending'),
            ('AKTIF', 'Aktif'),
            ('SELESAI', 'Selesai'),
        ),
        default='PENDING'
    )

    def __str__(self):
        return "%s %s" % (self.nama_kelas, self.tahun_ajaran)

    def clean(self):
        if not getattr(self, 'kurikulum', False):
            raise ValidationError({'kurikulum': 'silahkan pilih kurikulum'})

        if self.kurikulum.kelas != self.kelas:
            raise ValidationError({'kurikulum': 'Kelas pada kurikulum tidak sesuai'})

    def get_jadwal_pelajaran(self, current_day=True):
        mapel = self.mata_pelajaran_kelas.all()
        filters = {
                'kelas': self.id,
            }
        if current_day:
            filters['hari'] = timezone.now().weekday()
        return ItemJadwalPelajaran.objects.annotate(
                kelas = models.F('jadwal_kelas__kelas'),
                hari = models.F('jadwal_kelas__hari')
            ).filter(**filters)

    def get_jadwal_ekskul(self, current_day=True):
        filters = {
                'kelas': self.id,
            }
        if current_day:
            filters['hari'] = timezone.now().weekday()
        return ItemJadwalEkstraKurikuler.objects.annotate(
                kelas = models.F('jadwal_kelas__kelas'),
                hari = models.F('jadwal_kelas__hari')
            ).filter(**filters)


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


class JadwalKelas(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Kelas'
        verbose_name_plural = 'Jadwal Kelas'
        unique_together = ('hari', 'kelas')

    HARI = (
        (0, 'Senin'),
        (1, 'Selasa'),
        (2, 'Rabu'),
        (3, 'Kamis'),
        (4, 'Jumat'),
        (5, 'Sabtu'),
        (6, 'Minggu'),
    )
    hari = models.IntegerField(
        choices=HARI,
        default=1
    )
    kelas = models.ForeignKey(
        Kelas,
        on_delete=models.CASCADE,
        related_name='jadwal_kelas'
        )

    def __str__(self):
        return "%s %s" % (self.kelas, self.get_hari_display())


class ItemJadwalPelajaran(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Pelajaran'
        verbose_name_plural = 'Jadwal Pelajaran'
        unique_together = ('jadwal_kelas', 'mata_pelajaran')

    jadwal_kelas = models.ForeignKey(
        JadwalKelas,
        related_name='mata_pelajaran',
        on_delete=models.CASCADE
    )
    mata_pelajaran = models.ForeignKey(
        MataPelajaranKelas,
        on_delete=models.CASCADE,
        related_name='jadwal'
    )
    jam_mulai = models.TimeField(default=timezone.now)
    jam_berakhir = models.TimeField(default=timezone.now)
    deskripsi = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return "%s" % self.mata_pelajaran

    def clean(self):
        if self.jadwal_kelas.kelas != self.mata_pelajaran.kelas:
            raise ValidationError({'mata_pelajaran':'Pilih mata pelajaran sesuai kelas.'})


class ItemJadwalEkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Ekstra Kurikuler'
        verbose_name_plural = 'Jadwal Ekstra Kurikuler'

    jadwal_kelas = models.ForeignKey(
        JadwalKelas,
        related_name='ekskul',
        on_delete=models.CASCADE
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


class PresensiKelas(BaseModel):
    class Meta:
        verbose_name = 'Presensi Kelas'
        verbose_name_plural = 'Presensi Kelas'
        ordering = ['-tanggal']
        unique_together = ('kelas', 'tanggal')

    HARI = (
        (0, 'Senin'),
        (1, 'Selasa'),
        (2, 'Rabu'),
        (3, 'Kamis'),
        (4, 'Jumat'),
        (5, 'Sabtu'),
        (6, 'Minggu'),
    )

    kelas = models.ForeignKey(
        Kelas, on_delete=models.CASCADE,
        related_name='presensi'
        )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    tanggal = models.DateField(default=timezone.now)

    @cached_property
    def hari(self):
        return PresensiKelas.HARI[self.tanggal.weekday()][1]

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


class PiketKelas(BaseModel):
    class Meta:
        verbose_name = 'Piket Kelas'
        verbose_name_plural = 'Piket Kelas'
        unique_together = ('kelas', 'hari')

    HARI = (
        (0, 'Senin'),
        (1, 'Selasa'),
        (2, 'Rabu'),
        (3, 'Kamis'),
        (4, 'Jumat'),
        (5, 'Sabtu'),
        (6, 'Minggu'),
    )
    kelas = models.ForeignKey(
        Kelas, on_delete=models.CASCADE,
        related_name='piket')
    hari = models.IntegerField(
        choices=HARI,
        default=1
    )

    def __str__(self):
        return "%s %s" % (self.kelas, self.get_hari_display())


class ItemPiketKelas(BaseModel):
    class Meta:
        verbose_name = 'Item PiketKelas'
        verbose_name_plural = 'Item PiketKelas'
        unique_together = ('piket_kelas', 'siswa_kelas')

    piket_kelas = models.ForeignKey(
        PiketKelas, related_name='siswa_piket',
        on_delete=models.CASCADE
    )
    siswa_kelas = models.ForeignKey(
        SiswaKelas, related_name='piket_kelas',
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.piket_kelas, self.siswa_kelas)


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
        # create jadwal pelajaran kosong
        jadwal = []
        for hari in JadwalKelas.HARI:
            jadwal.append(JadwalKelas(
                kelas=instance,
                hari=hari[0]
            ))
        JadwalKelas.objects.bulk_create(jadwal)
        # create piket kelas kosong
        piket = []
        for hari in PiketKelas.HARI:
            piket.append(PiketKelas(
                kelas=instance,
                hari=hari[0]
            ))
        PiketKelas.objects.bulk_create(jadwal)
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