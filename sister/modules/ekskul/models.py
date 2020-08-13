from django.db import models
from sister.core.models import BaseModel
from sister.modules.kurikulum.models import TahunAjaran
from sister.modules.personal import Siswa


class EkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Ekstra Kurikuler'
        verbose_name_plural = 'Ekstra Kurikuler'

    nama = models.CharField(
        max_length=225,
        verbose_name='nama'
    )

    def __str__(self):
        return self.nama


class PesertaEkstraKurikuler(BaseModel):
    siswa = models.ForeignKey(
        Siswa,
        on_delete=models.CASCADE,
        related_name='penilaian_ekskul'
    )
    ekskul = models.ForeignKey(
        EkstraKurikuler,
        editable=True,
        on_delete=models.CASCADE,
        related_name='penilaian_ekskul'
        )
    tingkat = models.IntegerField()
    status = models.IntegerField()

    def __str__(self):
        return str(self.siswa)


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


class PenilaianEkstraKurikuler(BaseModel):
    class Meta:
        verbose_name = 'Penilaian Ekstra Kurikuler'
        verbose_name_plural = 'Penilaian Ekstra Kurikuler'
        unique_together = ('siswa', 'semester', 'ekskul')

    # tahun_ajaran = 
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )

    def __str__(self):
        return "Penilaian %s Ekskul %s semester %s" % (
            self.siswa, self.ekskul, self.semester
            )
