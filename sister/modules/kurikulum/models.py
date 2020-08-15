from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from sister.core.models import BaseModel
from .enums import KompetensiInti, KOMPETENSI_INTI_CHOICES


__all__ = [
    'Kurikulum',
    'MataPelajaran',
    'KompetensiDasar',
    'Tema',
]


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


class Kurikulum(BaseModel):
    class Meta:
        verbose_name = 'Kurikulum'
        verbose_name_plural = 'Kurikulum'
        unique_together = ('tahun', 'tingkat', 'kelas', 'revisi')

    kode = models.CharField(
        max_length=25, editable=False, unique=True)
    nama = models.CharField(max_length=225)
    tahun = models.IntegerField(default=0)
    tingkat = models.IntegerField(
        choices=[(x, x) for x in range(1, 10)],
        default=1
    )
    kelas = models.IntegerField(
        choices=[(x, x) for x in range(1, 13)],
        default=1
    )
    revisi = models.IntegerField(default=0)

    def __str__(self):
        return self.kode

    def generate_kode(self):
        return "K%s.T%s.K%s.R%s" % (
            self.tahun, self.tingkat, self.kelas, self.revisi
        )

    def save(self, *args, **kwargs):
        self.kode = self.generate_kode()
        super(Kurikulum, self).save(*args, **kwargs)


class MataPelajaran(BaseModel):
    class Meta:
        verbose_name = 'Mata Pelajaran'
        verbose_name_plural = 'Mata Pelajaran'

    kode = models.CharField(max_length=25)
    nama = models.CharField(max_length=225)
    mulok = models.BooleanField(default=False)

    def __str__(self):
        return "%s: %s" % (self.kode, self.nama)


class KurikulumMataPelajaran(BaseModel):
    class Meta:
        verbose_name = 'Kurikulum Mata Pelajaran'
        verbose_name_plural = 'Kurikulum Mata Pelajaran'
        unique_together = ('kurikulum', 'mata_pelajaran')

    kurikulum = models.ForeignKey(
        Kurikulum,
        related_name='mata_pelajaran',
        on_delete=models.CASCADE)
    mata_pelajaran = models.ForeignKey(
        MataPelajaran,
        related_name='kurikulum',
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.kurikulum, self.mata_pelajaran)


class KompetensiDasar(BaseModel):
    class Meta:
        verbose_name = 'Kompetensi Dasar'
        verbose_name_plural = 'Kompetensi Dasar'
        unique_together = (
            'kurikulum_mapel', 'ki', 'kd'
        )

    kurikulum_mapel = models.ForeignKey(
        KurikulumMataPelajaran,
        on_delete=models.CASCADE)
    ki = models.IntegerField(
        default=KompetensiInti.PENGETAHUAN.value,
        choices=KOMPETENSI_INTI_CHOICES,
        verbose_name='KI')
    kd = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='KD'
    )
    keyword = models.CharField(
        max_length=255,
        verbose_name=_('Keyword'),
        help_text="""
            Kata kunci menunjukkan kompetensi
            Contoh:'Mempraktekkan membaca Surat Al-Fatihah'.
            """
        )
    deskripsi = models.TextField(
        null=True, blank=True,
        verbose_name=_('Deskripsi')
        )

    @property
    def kode(self):
        return "%s %s.%s" % (
            self.kurikulum_mapel, self.ki, self.kd)

    def __str__(self):
        return self.kode


class Tema(BaseModel):
    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Tema'

    nomor = models.IntegerField()
    judul = models.CharField(max_length=225)
    deskripsi = models.TextField(null=True, blank=True)
    mata_pelajaran_kurikulum = models.ForeignKey(
        MataPelajaran,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s Tema %s" % (self.mata_pelajaran_kurikulum, self.nomor)
