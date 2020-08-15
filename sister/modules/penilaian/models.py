import pandas as pd
import numpy as np

from django.db import models
from django.db.utils import cached_property
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from sister.core.models import BaseModel
from sister.modules.kurikulum.models import KompetensiDasar
from sister.modules.kurikulum.enums import KompetensiInti
from sister.modules.pembelajaran.models import (
    SiswaKelas,
    MataPelajaranKelas,
    RentangNilai,
)
from .managers import PenilaianPembelajaranManager


__all__ = [
    'PenilaianPembelajaran',
    'ItemPenilaianTugas',
    'ItemPenilaianHarian',
    'ItemPenilaianTengahSemester',
    'ItemPenilaianAkhirSemester'
]


class MetodePenilaian:

    def __init__(self, penilaian):
        self.penilaian = penilaian

    def _get_kompetensi_scores(self):
        # Grab all Score by KD
        mapel_kelas = self.penilaian.mata_pelajaran
        kd_scores = KompetensiDasar.objects.filter(
            kurikulum_mapel=mapel_kelas.kurikulum_mapel
        ).annotate(
            x_tg=models.Subquery(
                self.penilaian.tugas.filter(
                    kompetensi=models.OuterRef('id')
                    ).values('nilai')
                ),
            x_ph=models.Subquery(
                self.penilaian.harian.filter(
                    kompetensi=models.OuterRef('id')
                    ).values('nilai')
                ),
            x_pts=models.Subquery(
                self.penilaian.tengah_semester.filter(
                    kompetensi=models.OuterRef('id')
                    ).values('nilai')
                ),
            x_pas=models.Subquery(
                self.penilaian.akhir_semester.filter(
                    kompetensi=models.OuterRef('id')
                    ).values('nilai')
                ),
        )
        return kd_scores

    def get_scores(self):
        raise NotImplementedError(
            "%s should implements get_scores",
            self.__class__.__name__
            )

    def get_rentang(self, nilai):
        try:
            rentang = RentangNilai.objects.get(
                kelas=self.penilaian.mata_pelajaran.kelas,
                nilai_minimum__lte=nilai,
                nilai_maximum__gte=nilai
            )
            return {
                'mutu': rentang.predikat,
                'predikat': rentang.get_predikat_display(),
                'aksi': rentang.get_aksi_display(),
            }
        except RentangNilai.DoesNotExist:
            return {
                'mutu': 'U',
                'predikat': 'belum teridentifikasi',
                'aksi': 'perlu penilaian',
            }

    def get_dataframe(self, kompetensi_inti=None):

        if not kompetensi_inti:
            return pd.DataFrame(self.get_scores()).replace({np.nan: None})
        else:
            if kompetensi_inti not in list(KompetensiInti):
                raise ValueError(
                    'Kompetensi Inti harus salah satu dari [1, 2, 3, 4]'
                )
            dataframe = pd.DataFrame(self.get_scores()).replace({np.nan: None})
            return dataframe.loc[dataframe['ki'] == kompetensi_inti.value]

    @property
    def nilai_spiritual(self):
        return self.get_dataframe(KompetensiInti.SIKAP_SPIRITUAL)

    @property
    def nilai_sosial(self):
        return self.get_dataframe(KompetensiInti.SIKAP_SOSIAL)

    @property
    def nilai_pengetahuan(self):
        return self.get_dataframe(KompetensiInti.PENGETAHUAN)

    @property
    def nilai_keterampilan(self):
        return self.get_dataframe(KompetensiInti.KETERAMPILAN)


class MetodePenilaianTerbobot(MetodePenilaian):

    def _score_weighting(self, kd_score):
        kd_score = kd_score.copy()
        bobot_tugas = self.penilaian.mata_pelajaran.bobot_tugas
        bobot_ph = self.penilaian.mata_pelajaran.bobot_ph
        bobot_pts = self.penilaian.mata_pelajaran.bobot_pts
        bobot_pas = self.penilaian.mata_pelajaran.bobot_pas

        kd_score['v_tg'] = (
            0
            if not kd_score['x_tg']
            else (kd_score['x_tg'] * bobot_tugas) / 100
            )
        kd_score['v_ph'] = (
            0
            if not kd_score['x_ph']
            else (kd_score['x_ph'] * bobot_ph) / 100
            )
        kd_score['v_pts'] = (
            0
            if not kd_score['x_pts']
            else (kd_score['x_pts'] * bobot_pts) / 100
            )
        kd_score['v_pas'] = (
            0
            if not kd_score['x_pas']
            else (kd_score['x_pas'] * bobot_pas) / 100
            )
        kd_score['total'] = (
            kd_score['v_tg']
            + kd_score['v_ph']
            + kd_score['v_pts']
            + kd_score['v_pas']
        )

        predicate = self.get_rentang(kd_score['total'])

        kd_score['mutu'] = predicate['mutu']
        kd_score['predikat'] = predicate['predikat']
        kd_score['deskripsi'] = " ".join([
            predicate['predikat'], 'dalam', kd_score['keyword'],
        ])

        return kd_score

    def get_scores(self):
        kd_scores = self._get_kompetensi_scores().values(
            'id', 'keyword', 'ki', 'kd', 'x_tg', 'x_ph', 'x_pts', 'x_pas',
        )
        weighted_scores = map(self._score_weighting, kd_scores)
        return list(weighted_scores)


class MetodeRataRata(MetodePenilaian):

    def _score_weighting(self, kd_score):
        kd_score = kd_score.copy()
        bobot_tugas = self.penilaian.mata_pelajaran.bobot_tugas
        bobot_ph = self.penilaian.mata_pelajaran.bobot_ph
        bobot_pts = self.penilaian.mata_pelajaran.bobot_pts
        bobot_pas = self.penilaian.mata_pelajaran.bobot_pas

        kd_score['v_tg'] = (
            0
            if not kd_score['x_tg']
            else (kd_score['x_tg'] * bobot_tugas) / 100
            )
        kd_score['v_ph'] = (
            0
            if not kd_score['x_ph']
            else (kd_score['x_ph'] * bobot_ph) / 100
            )
        kd_score['v_pts'] = (
            0
            if not kd_score['x_pts']
            else (kd_score['x_pts'] * bobot_pts) / 100
            )
        kd_score['v_pas'] = (
            0
            if not kd_score['x_pas']
            else (kd_score['x_pas'] * bobot_pas) / 100
            )
        kd_score['total'] = (
            kd_score['v_tg']
            + kd_score['v_ph']
            + kd_score['v_pts']
            + kd_score['v_pas']
        )

        predicate = self.get_rentang(kd_score['total'])

        kd_score['mutu'] = predicate['mutu']
        kd_score['predikat'] = predicate['predikat']
        kd_score['deskripsi'] = " ".join([
            predicate['predikat'], 'dalam', kd_score['keyword'],
        ])

        return kd_score

    def get_scores(self):
        kd_scores = self._get_kompetensi_scores().values(
            'id', 'keyword', 'ki', 'kd', 'x_tg', 'x_ph', 'x_pts', 'x_pas',
        )
        weighted_scores = map(self._score_weighting, kd_scores)
        return list(weighted_scores)


class PenilaianPembelajaran(BaseModel):
    class Meta:
        verbose_name = 'Penilaian Pembelajaran'
        verbose_name_plural = 'Penilaian Pembelajaran'

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

    kompetensi_tugas = models.ManyToManyField(
        KompetensiDasar, related_name='kompetensi_tugas')
    kompetensi_harian = models.ManyToManyField(
        KompetensiDasar, related_name='kompetensi_harian')
    kompetensi_tengah_semester = models.ManyToManyField(
        KompetensiDasar, related_name='kompetensi_tengah_semester')
    kompetensi_akhir_semester = models.ManyToManyField(
        KompetensiDasar, related_name='kompetensi_akhir_semester')

    def __str__(self):
        return "Penilaian %s %s semester %s" % (
            self.mata_pelajaran.mata_pelajaran,
            self.siswa, self.semester)

    def clean(self):
        siswa = getattr(self, 'siswa', None)
        mapel = getattr(self, 'mata_pelajaran', None)

        if not siswa:
            raise ValidationError({'siswa': 'Pilih siswa kelas'})
        if not mapel:
            raise ValidationError({
                'mata_pelajaran': 'Pilih mata pelajaran'
            })
        if siswa.kelas != mapel.kelas:
            raise ValidationError({
                'mata_pelajaran': 'Kelas siswa dan mata pelajaran tidak sesuai'
                })

    @property
    def metode(self):
        switch = {
            MataPelajaranKelas.METODE_RATA_RATA: MetodeRataRata,
            MataPelajaranKelas.METODE_TERBOBOT: MetodePenilaianTerbobot
        }
        metode_class = switch[self.mata_pelajaran.metode_penilaian]
        return metode_class(self)

    @cached_property
    def nilai_tg(self):
        return self.metode.dataframe['v_tg'].mean()

    @cached_property
    def nilai_ph(self):
        return self.metode.dataframe['v_ph'].mean()

    @cached_property
    def nilai_pts(self):
        return self.metode.dataframe['v_pts'].mean()

    @cached_property
    def nilai_pas(self):
        return self.metode.dataframe['v_pas'].mean()

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
        return self.get_rentang(self.nilai_total)['mutu']

    @cached_property
    def deskripsi(self):
        desc = ", ".join(self.dataframe['deskripsi'].values)
        return "%s %s" % (self.siswa.siswa, desc)


class ItemPenilaianTugas(BaseModel):
    class Meta:
        verbose_name = 'Penilaian Tugas'
        verbose_name_plural = 'Penilaian Tugas'
        unique_together = ('penilaian', 'kompetensi')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='tugas'
    )
    kompetensi = models.ForeignKey(
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

    def get_kompetensi_penilaian(self):
        return self.penilaian.kompetensi_tugas.all()

    def clean(self):
        if self.kompetensi not in self.get_kompetensi_penilaian():
            msg = {
                'kompetensi': "Kompetensi yang dipilih tidak "
                + "ada dalam daftar kompetensi penilaian tugas."
                }
            raise ValidationError(msg)


class ItemPenilaianHarian(BaseModel):
    class Meta:
        verbose_name = 'Penilaian Harian'
        verbose_name_plural = 'Penilaian Harian'
        unique_together = ('penilaian', 'kompetensi')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='harian'
    )
    kompetensi = models.ForeignKey(
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

    def get_kompetensi_penilaian(self):
        return self.penilaian.kompetensi_harian.all()

    def clean(self):
        if self.kompetensi not in self.get_kompetensi_penilaian():
            msg = {
                'kompetensi': "Kompetensi yang dipilih tidak "
                + "ada dalam daftar kompetensi penilaian harian."
                }
            raise ValidationError(msg)


class ItemPenilaianTengahSemester(BaseModel):
    class Meta:
        verbose_name = 'Penilaian Tengah Semester'
        verbose_name_plural = 'Penilaian Tengah Semester'
        unique_together = ('penilaian', 'kompetensi')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='tengah_semester'
    )
    kompetensi = models.ForeignKey(
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

    def get_kompetensi_penilaian(self):
        return self.penilaian.kompetensi_tengah_semester.all()

    def clean(self):
        if self.kompetensi not in self.get_kompetensi_penilaian():
            msg = {
                'kompetensi': "Kompetensi yang dipilih tidak "
                + "ada dalam daftar kompetensi penilaian tengah semester."
                }
            raise ValidationError(msg)


class ItemPenilaianAkhirSemester(BaseModel):
    class Meta:
        verbose_name = 'Penilaian Akhir Semester'
        verbose_name_plural = 'Penilaian Akhir Semester'
        unique_together = ('penilaian', 'kompetensi')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='akhir_semester'
    )
    kompetensi = models.ForeignKey(
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

    def get_kompetensi_penilaian(self):
        return self.penilaian.kompetensi_akhir_semester.all()

    def clean(self):
        if self.kompetensi not in self.get_kompetensi_penilaian():
            msg = {
                'kompetensi': "Kompetensi yang dipilih tidak "
                + "ada dalam daftar kompetensi penilaian akhir semester."
                }
            raise ValidationError(msg)
