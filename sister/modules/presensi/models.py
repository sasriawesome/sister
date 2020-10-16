from django.db import models
from django.db.models.signals import post_save
from django.db.utils import cached_property
from django.utils import timezone
from django.dispatch import receiver
from sister.modules.core.enums import Weekday
from sister.modules.core.models import BaseModel
from sister.modules.pembelajaran.models import Kelas, SiswaKelas

from .enums import PresensiStatus, PRESENSI_STATUS_CHOICES
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
    hari_libur = models.BooleanField(default=False)
    deskripsi = models.CharField(
        max_length=250,
        null=True, blank=True,
        help_text='Keterangan hari diliburkan, misal: Cuti bersama.'
    )

    @cached_property
    def hari(self):
        return Weekday.CHOICES.value[self.tanggal.weekday()][1]

    @cached_property
    def hadir(self):
        return self.presensi_siswa.filter(
                status=PresensiStatus.HADIR.value
            ).count()

    @cached_property
    def sakit(self):
        return self.presensi_siswa.filter(
                status=PresensiStatus.SAKIT.value
            ).count()

    @cached_property
    def izin(self):
        return self.presensi_siswa.filter(
                status=PresensiStatus.IZIN.value
            ).count()

    @cached_property
    def alfa(self):
        return self.presensi_siswa.filter(
                status=PresensiStatus.ALFA.value
            ).count()

    @cached_property
    def libur(self):
        return self.presensi_siswa.filter(
                status=PresensiStatus.LIBUR.value
            ).count()

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
        choices=PRESENSI_STATUS_CHOICES,
        default=PresensiStatus.HADIR.value
    )

    def __str__(self):
        return "%s %s" % (self.presensi_kelas, self.siswa_kelas)


@receiver(post_save, sender=PresensiKelas)
def after_save_presensi_siswa(sender, **kwargs):
    created = kwargs.pop('created', None)
    instance = kwargs.pop('instance', None)
    if instance.hari_libur:
        status = PresensiStatus.LIBUR.value
    else:
        status = PresensiStatus.HADIR.value
    if created:
        # add initial items
        items = []
        for siswa in instance.kelas.siswa.all():
            items.append(
                PresensiSiswa(
                    siswa_kelas=siswa,
                    presensi_kelas=instance,
                    status=status
                )
            )
        PresensiSiswa.objects.bulk_create(items)
    else:
        instance.presensi_siswa.update(status=status)
