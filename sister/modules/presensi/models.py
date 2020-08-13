from django.db import models
from django.db.models.signals import post_save
from django.db.utils import cached_property
from django.utils import timezone
from django.dispatch import receiver
from sister.core.enums import Weekday
from sister.core.models import BaseModel
from sister.modules.pembelajaran.models import Kelas, SiswaKelas
from sister.modules.kurikulum.enums import (
    AktifitasPendidikan,
    AKTIFITAS_CHOICES
    )

from .managers import PresensiKelasManager, PresensiSiswaManager


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
        choices=AKTIFITAS_CHOICES,
        default=AktifitasPendidikan.HARI_SEKOLAH_EFEKTIF.value,
        help_text='Alasan kelas diliburkan, atau catatan lain.'
    )
    deskripsi = models.CharField(
        max_length=250,
        null=True, blank=True,
        help_text='Penjelasan aktifitas.'
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
            ('A', 'Alfa'),
        ),
        default='H'
    )

    def __str__(self):
        return "%s %s" % (self.presensi_kelas, self.siswa_kelas)


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
