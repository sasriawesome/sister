import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from sister.core.enums import MaxLength
from sister.core.models import BaseModel, SimpleBaseModel


__all__ = [
    # 'Sekolah',
    'TahunAjaran',
    'EkstraKurikuler',
    'Kurikulum',
    'MataPelajaran',
    'MataPelajaranKurikulum'
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


class EkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Ekstra Kurikuler'
        verbose_name_plural = 'Ekstra Kurikuler'

    nama = models.CharField(
        max_length=225,
        verbose_name=_('nama')
    )

    def __str__(self):
        return self.nama
