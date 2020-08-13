from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from sister.core.models import BaseModel

__all__ = [
    # 'Sekolah',
    'Kurikulum',
    'MataPelajaran',
    'MataPelajaranKurikulum',
    'KompetensiInti',
    'KompetensiDasar',
    'Tema',
]

# class Sekolah(BaseModel):
#     class Meta:
#         verbose_name = 'Sekolah'
#         verbose_name_plural = 'Sekolah'

#     npsn = models.CharField(max_length=25)
#     nss = models.CharField(max_length=25)
#     nama_sekolah = models.CharField(max_length=225)

#     def __str__(self):
#         return self.nama_sekolah


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


class MataPelajaranKurikulum(BaseModel):
    class Meta:
        verbose_name = 'Mata Pelajaran Kurikulum'
        verbose_name_plural = 'Mata Pelajaran Kurikulum'

    mata_pelajaran = models.ForeignKey(
        MataPelajaran,
        on_delete=models.CASCADE)
    kurikulum = models.ForeignKey(
        Kurikulum,
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s.%s" % (self.kurikulum, self.mata_pelajaran)


class KompetensiInti(BaseModel):
    class Meta:
        verbose_name = 'Kompetensi Inti'
        verbose_name_plural = 'Kompetensi Inti'

    nomor = models.IntegerField()
    deskripsi = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return "%s. %s" % (self.nomor, self.deskripsi)


class KompetensiDasar(BaseModel):
    class Meta:
        verbose_name = 'Kompetensi Dasar'
        verbose_name_plural = 'Kompetensi Dasar'
        unique_together = (
            'mata_pelajaran_kurikulum',
            'kompetensi_inti',
            'nomor'
        )

    mata_pelajaran_kurikulum = models.ForeignKey(
        MataPelajaranKurikulum,
        on_delete=models.CASCADE)
    kompetensi_inti = models.ForeignKey(
        KompetensiInti,
        on_delete=models.CASCADE
    )
    nomor = models.IntegerField()
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    keyword = models.CharField(
        max_length=255,
        verbose_name=_('Kata kunci')
        )
    deskripsi = models.TextField(
        verbose_name=_('Kata kunci')
        )
    ph = models.BooleanField(default=True)
    pts = models.BooleanField(default=False)
    pas = models.BooleanField(default=True)

    @property
    def kode(self):
        return "%s.%s" % (self.kompetensi_inti.nomor, self.nomor)

    def __str__(self):
        return "%s KD %s" % (
            self.mata_pelajaran_kurikulum,
            self.kode
        )


class Tema(BaseModel):
    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Tema'

    nomor = models.IntegerField()
    judul = models.CharField(max_length=225)
    deskripsi = models.TextField(null=True, blank=True)
    mata_pelajaran_kurikulum = models.ForeignKey(
        MataPelajaranKurikulum,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s Tema %s" % (self.mata_pelajaran_kurikulum, self.nomor)
