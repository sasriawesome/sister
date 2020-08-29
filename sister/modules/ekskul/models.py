from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator, MinLengthValidator
from sister.core.models import BaseModel
from sister.core.enums import Weekday, WEEKDAY_CHOICES
from sister.modules.kurikulum.models import TahunAjaran
from sister.modules.personal.models import Siswa, Guru


class EkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Ekstra Kurikuler'
        verbose_name_plural = 'Ekstra Kurikuler'

    nama = models.CharField(
        max_length=225,
        verbose_name='nama'
    )
    deskripsi = models.TextField(
        max_length=225,
        verbose_name='deskripsi'
    )

    def __str__(self):
        return self.nama


class TahunAngkatan(BaseModel):
    class Meta:
        verbose_name = 'Tahun Angkatan'
        verbose_name_plural = 'Tahun Angkatan'

    pembina = models.ForeignKey(
        Guru,
        on_delete=models.CASCADE,
        related_name='pembina_ekskul'
        )
    pembina = models.ForeignKey(
        Guru,
        on_delete=models.CASCADE,
        related_name='pembina_ekskul'
        )
    tahun_ajaran = models.ForeignKey(
        TahunAjaran,
        on_delete=models.CASCADE,
        related_name='angkatan'
        )
    ekskul = models.ForeignKey(
        EkstraKurikuler,
        on_delete=models.CASCADE,
        related_name='angkatan'
        )
    tingkat = models.CharField(
        max_length=125,
        null=True, blank=True
    )

    def __str__(self):
        return "%s %s" % (self.ekskul, self.tahun_ajaran)


class PesertaEkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Peserta Ekskul'
        verbose_name_plural = 'Peserta Ekskul'
        unique_together = ('siswa', 'tahun_angkatan')
    siswa = models.ForeignKey(
        Siswa,
        on_delete=models.CASCADE,
        related_name='peserta_ekskul'
    )
    tahun_angkatan = models.ForeignKey(
        TahunAngkatan,
        editable=True,
        on_delete=models.CASCADE,
        related_name='peserta_ekskul'
        )
    tingkat = models.IntegerField(
        editable=False, default=1)
    status = models.IntegerField(
        choices=(
            (1, 'Aktif'),
            (2, 'Alumni'),
            (99, 'Keluar'),
        ),
        default=1
    )

    def __str__(self):
        return str(self.siswa)


class PenilaianEkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Penilaian Ekstra Kurikuler'
        verbose_name_plural = 'Penilaian Ekstra Kurikuler'
        unique_together = ('peserta', 'tahun_ajaran', 'semester')

    peserta = models.ForeignKey(
        PesertaEkstraKurikuler,
        on_delete=models.CASCADE,
        related_name='penilaian_ekskul'
    )
    tahun_ajaran = models.ForeignKey(
        TahunAjaran,
        on_delete=models.CASCADE,
        related_name='penilaian_ekskul'
        )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    nilai = models.IntegerField(
        default=60,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(100)
        ]
    )
    predikat = models.CharField(
        max_length=1,
        choices=(
            ('A', 'Sangat Baik'),
            ('B', 'Baik'),
            ('C', 'Cukup Baik'),
            ('D', 'Kurang Baik'),
        )
    )
    deskripsi = models.TextField()


class JadwalEkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Jadwal Ekstra Kurikuler'
        verbose_name_plural = 'Jadwal Ekstra Kurikuler'
        unique_together = (
            'hari', 'semester', 'tahun_ajaran', 'ekstrakurikuler')

    ekstrakurikuler = models.ForeignKey(
        EkstraKurikuler,
        on_delete=models.CASCADE,
        related_name='jadwal'
    )
    tahun_ajaran = models.ForeignKey(
        TahunAjaran,
        on_delete=models.CASCADE,
        related_name='jadwal_ekskul'
        )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    hari = models.IntegerField(
        choices=WEEKDAY_CHOICES,
        default=Weekday.MONDAY.value
    )
    jam_mulai = models.TimeField(default=timezone.now)
    jam_berakhir = models.TimeField(default=timezone.now)
    deskripsi = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return "%s" % self.ekstra_kurikuler
