import pandas as pd
import numpy as np

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from sister.core.models import BaseModel
from sister.modules.kurikulum.models import KompetensiDasar
from sister.modules.kurikulum.enums import KompetensiInti
from sister.modules.pembelajaran.models import (
    SiswaKelas,
    MataPelajaranKelas,
    RentangNilai,
    KompetensiPenilaian
)
from .managers import PenilaianPembelajaranManager
from .enums import JENIS_PENILAIAN_CHOICES, JenisPenilaian


__all__ = [
    'PenilaianPembelajaran',
    'ItemPenilaian'
]


class MetodePenilaian:

    kd_score_column = (
        'id', 'keyword', 'tgs', 'ph', 'pts', 'pas',
        'ki', 'kd', 'x_tg', 'x_ph', 'x_pts', 'x_pas',
    )

    def __init__(self, penilaian):
        self.penilaian = penilaian

    def _get_kompetensi_scores(self):
        # Grab all Score by KD
        kompetensi = self.penilaian.mata_pelajaran.kompetensi_penilaian
        kd_scores = kompetensi.annotate(
            keyword=models.F('kompetensi__keyword'),
            ki=models.F('kompetensi__ki'),
            kd=models.F('kompetensi__kd'),
            x_tg=models.Subquery(
                self.penilaian.nilai.filter(
                    kompetensi=models.OuterRef('kompetensi_id'),
                    jenis_penilaian=JenisPenilaian.TUGAS.value,
                ).values('nilai')
            ),
            x_ph=models.Subquery(
                self.penilaian.nilai.filter(
                    kompetensi=models.OuterRef('kompetensi_id'),
                    jenis_penilaian=JenisPenilaian.PH.value,
                ).values('nilai')
            ),
            x_pts=models.Subquery(
                self.penilaian.nilai.filter(
                    kompetensi=models.OuterRef('kompetensi_id'),
                    jenis_penilaian=JenisPenilaian.PTS.value,
                ).values('nilai')
            ),
            x_pas=models.Subquery(
                self.penilaian.nilai.filter(
                    kompetensi=models.OuterRef('kompetensi_id'),
                    jenis_penilaian=JenisPenilaian.PAS.value,
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
        scores = self.get_scores()
        if not bool(scores):
            extra_column = ('mutu',)
            return pd.DataFrame(columns=self.kd_score_column + extra_column)
        if not kompetensi_inti:
            return pd.DataFrame(scores).replace({np.nan: None})
        else:
            if kompetensi_inti not in list(KompetensiInti):
                raise ValueError(
                    'Kompetensi Inti harus salah satu dari [1, 2, 3, 4]'
                )
            dataframe = pd.DataFrame(scores).replace({np.nan: None})
            return dataframe.loc[dataframe['ki'] == kompetensi_inti.value]

    def build_final_score(self, kompetensi_inti):
        df = self.get_dataframe(kompetensi_inti)
        if df.empty:
            return 0
        return df['total'].mean()

    def build_final_predicate(self, kompetensi_inti):
        score = self.build_final_score(kompetensi_inti)
        return self.get_rentang(score)

    def build_final_desc(self, kompetensi_inti):
        df = self.get_dataframe(kompetensi_inti)
        df = pd.concat([
                df.loc[df['mutu'] == 'A'],
                df.loc[df['mutu'] == 'B'],
                df.loc[df['mutu'] == 'C']
            ])
        if df.empty:
            deskripsi = 'masih perlu penilaian.'
        else:
            df['deskripsi'] = df['predikat'] + ' dalam ' + df['keyword']
            deskripsi = ", ".join(df['deskripsi'])
        return 'Ananda ' + deskripsi

    def build_final_recomendation(self, kompetensi_inti):
        df = self.get_dataframe(kompetensi_inti)
        df = pd.concat([
                df.loc[df['mutu'] == 'C'],
                df.loc[df['mutu'] == 'D'],
                df.loc[df['mutu'] == 'E'],
                df.loc[df['mutu'] == 'U']
            ])
        predikat = self.build_final_predicate(kompetensi_inti)
        if df.empty:
            rekomendasi = 'masih perlu penilaian.'
        else:
            df['deskripsi'] = predikat['aksi'] + ' dalam ' + df['keyword']
            rekomendasi = ", ".join(df['deskripsi'])
        return 'Ananda ' + rekomendasi

    def build_final_report(self, kompetensi_inti):
        predikat = self.build_final_predicate(kompetensi_inti)
        return {
                'data': self.get_dataframe(kompetensi_inti),
                'score': self.build_final_score(kompetensi_inti),
                'mutu': predikat['mutu'],
                'predikat': predikat['predikat'],
                'deskripsi': self.build_final_desc(kompetensi_inti),
                'rekomendasi': self.build_final_recomendation(kompetensi_inti)
            }


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
        kd_score['aksi'] = predicate['aksi']
        kd_score['deskripsi'] = " ".join([
            predicate['predikat'], 'dalam', kd_score['keyword'],
        ])

        return kd_score

    def get_scores(self):
        kd_scores = self._get_kompetensi_scores().values(*self.kd_score_column)
        weighted_scores = map(self._score_weighting, kd_scores)
        return list(weighted_scores)


class MetodeRataRata(MetodePenilaian):

    def _get_v_score(self, x_score):
        v_score = 0
        if x_score:
            v_score = x_score
        return v_score

    def get_kd_denominator(self, kompetensi_penilaian):
        denominator = 0
        if kompetensi_penilaian['tgs']:
            denominator += 1
        if kompetensi_penilaian['ph']:
            denominator += 1
        if kompetensi_penilaian['pts']:
            denominator += 1
        if kompetensi_penilaian['pas']:
            denominator += 1
        if denominator == 0:
            denominator = 1
        return denominator

    def _score_weighting(self, kd_score):
        kd_score = kd_score.copy()
        kd_score['v_tg'] = self._get_v_score(kd_score['x_tg'])
        kd_score['v_ph'] = self._get_v_score(kd_score['x_ph'])
        kd_score['v_pts'] = self._get_v_score(kd_score['x_pts'])
        kd_score['v_pas'] = self._get_v_score(kd_score['x_pas'])

        kd_score['total'] = (
            kd_score['v_tg']
            + kd_score['v_ph']
            + kd_score['v_pts']
            + kd_score['v_pas']
        ) / self.get_kd_denominator(kd_score)

        predicate = self.get_rentang(kd_score['total'])

        kd_score['mutu'] = predicate['mutu']
        kd_score['predikat'] = predicate['predikat']
        kd_score['deskripsi'] = " ".join([
            predicate['predikat'], 'dalam', kd_score['keyword'],
        ])
        return kd_score

    def get_scores(self):
        kd_scores = self._get_kompetensi_scores().values(*self.kd_score_column)
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

    @property
    def nilai_spiritual(self):
        nilai = self.metode.build_final_report(KompetensiInti.SIKAP_SPIRITUAL)
        nilai.update({'kompetensi': None})
        return nilai

    @property
    def nilai_sosial(self):
        nilai = self.metode.build_final_report(KompetensiInti.SIKAP_SOSIAL)
        nilai.update({'kompetensi': None})
        return nilai

    @property
    def nilai_pengetahuan(self):
        nilai = self.metode.build_final_report(KompetensiInti.PENGETAHUAN)
        nilai.update({
            'kompetensi': 'Mengingat dan memahami '
                          + 'pengetahuan faktual dan konsep '
                          + '%s' % self.mata_pelajaran.mata_pelajaran.nama
        })
        return nilai

    @property
    def nilai_keterampilan(self):
        nilai = self.metode.build_final_report(KompetensiInti.KETERAMPILAN)
        nilai.update({
            'kompetensi': 'Menyajikan pengetahuan dan keterampilan '
                          + 'dalam pembelajaran '
                          + '%s' % self.mata_pelajaran.mata_pelajaran.nama
        })
        return nilai

    def get_nilai_qs(self):
        qs = self.nilai.all()
        return qs


class ItemPenilaian(BaseModel):
    class Meta:
        verbose_name = 'Item Penilaian'
        verbose_name_plural = 'Item Penilaian'
        ordering = ['jenis_penilaian', 'kompetensi__ki', 'kompetensi__kd']
        unique_together = ('jenis_penilaian', 'penilaian', 'kompetensi')

    penilaian = models.ForeignKey(
        PenilaianPembelajaran,
        on_delete=models.CASCADE,
        related_name='nilai'
    )
    jenis_penilaian = models.IntegerField(
        choices=JENIS_PENILAIAN_CHOICES,
        default=JenisPenilaian.PH.value,
        verbose_name='Jenis Penilaian'
    )
    kompetensi = models.ForeignKey(
        KompetensiDasar,
        on_delete=models.PROTECT,
        related_name='item_penilaian'
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    def kompetensi_inti(self):
        return self.kompetensi.ki

    def get_kompetensi_dasar(self, jenis_penilaian=None):
        switch_filters = {
            JenisPenilaian.TUGAS: {'tgs': True},
            JenisPenilaian.PH: {'ph': True},
            JenisPenilaian.PTS: {'pts': True},
            JenisPenilaian.PAS: {'pas': True},
        }
        kompetensi = self.penilaian.mata_pelajaran.kompetensi_penilaian
        filters = switch_filters.get(jenis_penilaian, {})
        return kompetensi.filter(**filters)

    def validate_kompetensi(self, jenis_penilaian):
        try:
            self.get_kompetensi_dasar(
                jenis_penilaian
            ).get(
                kompetensi=self.kompetensi
            )
        except KompetensiPenilaian.DoesNotExist:
            msg = {
                'kompetensi': "Kompetensi yang dipilih tidak "
                + "ada dalam daftar kompetensi penilaian "
                + "%s." % self.get_jenis_penilaian_display()
            }
            raise ValidationError(msg)

    def clean(self):
        if self.jenis_penilaian == JenisPenilaian.TUGAS.value:
            self.validate_kompetensi(JenisPenilaian.TUGAS)
        if self.jenis_penilaian == JenisPenilaian.PH.value:
            self.validate_kompetensi(JenisPenilaian.PH)
        if self.jenis_penilaian == JenisPenilaian.PTS.value:
            self.validate_kompetensi(JenisPenilaian.PTS)
        if self.jenis_penilaian == JenisPenilaian.PAS.value:
            self.validate_kompetensi(JenisPenilaian.PAS)
