import uuid
import pandas as pd

from django.db import models
from django.db.models.functions import Coalesce
from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from polymorphic.models import PolymorphicModel

from sister.core.enums import MaxLength
from sister.core.models import BaseModel, SimpleBaseModel
from sister.modules.kurikulum.models import *
from sister.modules.pembelajaran.models import *
from .managers import PenilaianPembelajaranManager


__all__ = [
    'Penilaian',
    'PenilaianPembelajaran',
    'ItemPenilaianTugas',
    'ItemPenilaianHarian',
    'ItemPenilaianTengahSemester',
    'ItemPenilaianAkhirSemester',
    'PenilaianEkstraKurikuler'
]


class Penilaian(PolymorphicModel, BaseModel):
    class Meta:
        verbose_name = _('Penilaian')
        verbose_name_plural = _('Penilaian')

    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


class PenilaianPembelajaran(Penilaian):
    class Meta:
        verbose_name = _('Penilaian Pembelajaran')
        verbose_name_plural = _('Penilaian Pembelajaran')

    objects = PenilaianPembelajaranManager()
    
    siswa = models.ForeignKey(
        SiswaKelas, 
        on_delete=models.CASCADE,
        related_name='penilaian_pembelajaran'
    )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    mata_pelajaran = models.ForeignKey(
        MataPelajaranKelas,
        on_delete=models.CASCADE,
        related_name='penilaian_pembelajaran'
    )

    @cached_property
    def mapel_kurikulum(self):
        try:
            mpk = MataPelajaranKurikulum.objects.get(
                mata_pelajaran=self.mata_pelajaran.mata_pelajaran,
                kurikulum=self.mata_pelajaran.kelas.kurikulum
                )
            return mpk
        except MataPelajaranKurikulum.DoesNotExist:
            return None

    def __str__(self):
        return "Penilaian %s %s" % (self.mata_pelajaran.mata_pelajaran, self.siswa)

    def clean(self):
        siswa = getattr(self, 'siswa', None)
        mapel = getattr(self, 'mata_pelajaran', None)
        
        if not siswa:
            raise ValidationError({'siswa': 'Pilih siswa kelas'})
        if not mapel:
            raise ValidationError({'mata_pelajaran':'Pilih mata pelajaran'})
        if siswa.kelas != mapel.kelas:
            raise ValidationError({'mata_pelajaran':'Kelas siswa dan mata pelajaran kelas tidak sesuai'})
    

    def get_nilai_kd_scores(self):
        # Grab all Score by KD
        kd_mapel = self.mapel_kurikulum.kompetensidasar_set
        kd_scores = kd_mapel.filter(
            semester=self.semester
        ).annotate(
            ki = models.F('kompetensi_inti__nomor'),
            kd = models.F('nomor'),
            x_tg = models.Subquery(
                self.tugas.filter(
                    kompetensi_dasar=models.OuterRef('id')).values('nilai')),
            x_ph = models.Subquery(
                     self.harian.filter(
                    kompetensi_dasar=models.OuterRef('id')).values('nilai')),
            x_pts = models.Subquery(
                self.tengah_semester.filter(
                    kompetensi_dasar=models.OuterRef('id')).values('nilai')),
            x_pas =models.Subquery(
                self.akhir_semester.filter(
                    kompetensi_dasar=models.OuterRef('id')).values('nilai')),
        )
        return kd_scores

    def _get_rentang(self, nilai):
        try:
            rentang = RentangNilai.objects.get(
                kelas=self.mata_pelajaran.kelas,
                nilai_minimum__lte=nilai,
                nilai_maximum__gte=nilai
            )
            return {
                'mutu': rentang.predikat,
                'predikat': rentang.get_predikat_display(),
                'aksi': rentang.get_aksi_display(),
                
            }
        except:
            return {
                'mutu': 'U',
                'predikat': 'belum teridentifikasi',
                'aksi': 'perlu penilaian',   
            }

    def _score_weighting(self, kd_score):
            kd_score = kd_score.copy()
            bobot_tugas = self.mata_pelajaran.tugas
            bobot_ph = self.mata_pelajaran.ph
            bobot_pts = self.mata_pelajaran.pts
            bobot_pas = self.mata_pelajaran.pas
            
            if not kd_score['pts']:
                bobot_ph += bobot_pts / 2
                bobot_pas += bobot_pts / 2
                bobot_pts = 0

            kd_score['v_tg'] = 0 if not kd_score['x_tg'] else (kd_score['x_tg'] * bobot_tugas) / 100
            kd_score['v_ph'] = 0 if not kd_score['x_ph'] else (kd_score['x_ph'] * bobot_ph) / 100
            kd_score['v_pts'] = 0 if not kd_score['x_pts'] else (kd_score['x_pts'] * bobot_pts) / 100
            kd_score['v_pas'] = 0 if not kd_score['x_pas'] else (kd_score['x_pas'] * bobot_pas) / 100
            kd_score['total'] = kd_score['v_tg'] + kd_score['v_ph'] + kd_score['v_pts'] + kd_score['v_pas']
            
            predicate = self._get_rentang(kd_score['total'])
            
            kd_score['mutu'] = predicate['mutu']
            kd_score['predikat'] = predicate['predikat']
            kd_score['deskripsi'] = " ".join([
                predicate['predikat'], 'dalam',kd_score['keyword'],
            ])
            
            return kd_score

    def get_weighted_kd_scores(self):
        kd_scores = self.get_nilai_kd_scores().values(
            'id','keyword', 'ki', 'kd', 'ph', 'pts', 'pas', 'x_tg', 'x_ph', 'x_pts', 'x_pas',
        )
        weighted_scores = map(self._score_weighting, kd_scores)
        return list(weighted_scores)

    @cached_property
    def dataframe(self):
        return pd.DataFrame(self.get_weighted_kd_scores())

    @cached_property
    def nilai_tugas(self):
        return self.dataframe['v_tg'].mean()

    @cached_property
    def nilai_ph(self):
        return self.dataframe['v_ph'].mean()

    @cached_property
    def nilai_pts(self):
        return self.dataframe['v_pts'].mean()

    @cached_property
    def nilai_pas(self):
        return self.dataframe['v_pas'].mean()

    @cached_property
    def nilai_total(self):
        return round(
            self.nilai_tugas
            + self.nilai_ph 
            + self.nilai_pts 
            + self.nilai_pas
            )

    @cached_property
    def predikat(self):
        return self._get_rentang(self.nilai_total)['mutu']

    @cached_property
    def deskripsi(self):
        desc = ", ".join(self.dataframe['deskripsi'].values)
        return "%s %s" % (self.siswa.siswa, desc) 


class ItemPenilaianTugas(BaseModel):
    class Meta:
        verbose_name = _('Penilaian Tugas')
        verbose_name_plural = _('Penilaian Tugas')
        unique_together = ('penilaian', 'kompetensi_dasar')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='tugas'
    )
    kompetensi_dasar = models.ForeignKey(
        KompetensiDasar,
        on_delete=models.PROTECT,
        related_name='tugas'
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


class ItemPenilaianHarian(BaseModel):
    class Meta:
        verbose_name = _('Penilaian Harian')
        verbose_name_plural = _('Penilaian Harian')
        unique_together = ('penilaian', 'kompetensi_dasar')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='harian'
    )
    kompetensi_dasar = models.ForeignKey(
        KompetensiDasar,
        on_delete=models.PROTECT,
        related_name='harian'
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


class ItemPenilaianTengahSemester(BaseModel):
    class Meta:
        verbose_name = _('Penilaian Tengah Semester')
        verbose_name_plural = _('Penilaian Tengah Semester')
        unique_together = ('penilaian', 'kompetensi_dasar')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='tengah_semester'
    )
    kompetensi_dasar = models.ForeignKey(
        KompetensiDasar,
        on_delete=models.PROTECT,
        related_name='tengah_semester'
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


class ItemPenilaianAkhirSemester(BaseModel):
    class Meta:
        verbose_name = _('Penilaian Akhir Semester')
        verbose_name_plural = _('Penilaian Akhir Semester')
        unique_together = ('penilaian', 'kompetensi_dasar')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='akhir_semester'
    )
    kompetensi_dasar = models.ForeignKey(
        KompetensiDasar,
        on_delete=models.PROTECT,
        related_name='akhir_semester'
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


class PenilaianEkstraKurikuler(Penilaian):
    class Meta:
        verbose_name = 'Penilaian Ekstra Kurikuler'
        verbose_name_plural = 'Penilaian Ekstra Kurikuler'
        unique_together = ('siswa', 'semester', 'ekskul')

    siswa = models.ForeignKey(
        SiswaKelas, 
        on_delete=models.CASCADE,
        related_name='penilaian_ekskul'
    )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    ekskul = models.ForeignKey(
        EkstraKurikuler,
        editable=True,
        on_delete=models.CASCADE,
        related_name='penilaian_ekskul'
        )

    def __str__(self):
        return "Penilaian %s Ekskul %s semester %s" % (self.siswa, self.ekskul, self.semester)