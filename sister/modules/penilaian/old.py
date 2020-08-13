class NilaiMataPelajaran(PolymorphicModel, BaseModel):
    class Meta:
        verbose_name = 'Nilai Mata Pelajaran'
        verbose_name_plural = 'Nilai Pelajaran'
        # unique_together = ('siswa_kelas', 'mata_pelajaran_kelas')

    no_urut = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    kkm = models.IntegerField(
        default=65,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )


class NilaiMataPelajaranKTSP(NilaiMataPelajaran):
    class Meta:
        verbose_name = 'Nilai Mata Pelajaran KTSP'
        verbose_name_plural = 'Nilai Mata Pelajaran KTSP'

    siswa_kelas = models.ForeignKey(
        SiswaKelas,
        on_delete=models.CASCADE,
        related_name='nilai_mata_pelajaran_ktsp'
    )
    mata_pelajaran_kelas = models.ForeignKey(
        MataPelajaranKelas,
        on_delete=models.CASCADE,
        related_name='nilai_mata_pelajaran_ktps'
    )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    deskripsi = models.TextField()


class NilaiMataPelajaranK13(NilaiMataPelajaran):
    class Meta:
        verbose_name = 'Nilai Mata Pelajaran K13'
        verbose_name_plural = 'Nilai Mata Pelajaran K13'
        unique_together = (
            'siswa_kelas',
            'mata_pelajaran_kelas',
            'semester',
            'kompetensi'
        )

    SPIRITUAL = 1
    SOSIAL = 2
    PENGETAHUAN = 3
    KETERAMPILAN = 4
    KOMPETENSI = (
        (1, 'Sikap Spiritual'),
        (2, 'Sikap Sosial'),
        (3, 'Pengetahuan'),
        (4, 'Keterampilan'),
    )
    siswa_kelas = models.ForeignKey(
        SiswaKelas,
        on_delete=models.CASCADE,
        related_name='nilai_mata_pelajaran_k13'
    )
    mata_pelajaran_kelas = models.ForeignKey(
        MataPelajaranKelas,
        on_delete=models.CASCADE,
        related_name='nilai_mata_pelajaran_k13'
    )
    semester = models.IntegerField(
        choices=((1, 1), (2, 2),),
        default=1
    )
    kompetensi = models.IntegerField(
        default=PENGETAHUAN,
        choices=KOMPETENSI
    )
    nilai = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    deskripsi = models.TextField()

