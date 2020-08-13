# Generated by Django 3.0.8 on 2020-08-13 13:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KompetensiInti',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('nomor', models.IntegerField()),
                ('deskripsi', models.CharField(blank=True, max_length=225, null=True)),
            ],
            options={
                'verbose_name': 'Kompetensi Inti',
                'verbose_name_plural': 'Kompetensi Inti',
            },
        ),
        migrations.CreateModel(
            name='Kurikulum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('kode', models.CharField(editable=False, max_length=25, unique=True)),
                ('nama', models.CharField(max_length=225)),
                ('tahun', models.IntegerField(default=0)),
                ('tingkat', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], default=1)),
                ('kelas', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], default=1)),
                ('revisi', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Kurikulum',
                'verbose_name_plural': 'Kurikulum',
                'unique_together': {('tahun', 'tingkat', 'kelas', 'revisi')},
            },
        ),
        migrations.CreateModel(
            name='MataPelajaran',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('kode', models.CharField(max_length=25)),
                ('nama', models.CharField(max_length=225)),
                ('mulok', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Mata Pelajaran',
                'verbose_name_plural': 'Mata Pelajaran',
            },
        ),
        migrations.CreateModel(
            name='MataPelajaranKurikulum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('kurikulum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.Kurikulum')),
                ('mata_pelajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.MataPelajaran')),
            ],
            options={
                'verbose_name': 'Mata Pelajaran Kurikulum',
                'verbose_name_plural': 'Mata Pelajaran Kurikulum',
            },
        ),
        migrations.CreateModel(
            name='TahunAjaran',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('kode', models.CharField(editable=False, max_length=10, unique=True)),
                ('tahun_mulai', models.IntegerField(validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(3000)])),
                ('bulan_mulai', models.IntegerField(choices=[(1, 'Januari'), (2, 'Februari'), (3, 'Maret'), (4, 'April'), (5, 'Mei'), (6, 'Juni'), (7, 'Juli'), (8, 'Agustus'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'Desember')], default=7)),
                ('tahun_akhir', models.IntegerField(validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(3000)])),
                ('bulan_akhir', models.IntegerField(choices=[(1, 'Januari'), (2, 'Februari'), (3, 'Maret'), (4, 'April'), (5, 'Mei'), (6, 'Juni'), (7, 'Juli'), (8, 'Agustus'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'Desember')], default=6)),
            ],
            options={
                'verbose_name': 'Tahun Ajaran',
                'verbose_name_plural': 'Tahun Ajaran',
            },
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('nomor', models.IntegerField()),
                ('judul', models.CharField(max_length=225)),
                ('deskripsi', models.TextField(blank=True, null=True)),
                ('mata_pelajaran_kurikulum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.MataPelajaranKurikulum')),
            ],
            options={
                'verbose_name': 'Tema',
                'verbose_name_plural': 'Tema',
            },
        ),
        migrations.CreateModel(
            name='KompetensiDasar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('nomor', models.IntegerField()),
                ('semester', models.IntegerField(choices=[(1, 1), (2, 2)], default=1)),
                ('keyword', models.CharField(max_length=255, verbose_name='Kata kunci')),
                ('deskripsi', models.TextField(verbose_name='Kata kunci')),
                ('ph', models.BooleanField(default=True)),
                ('pts', models.BooleanField(default=False)),
                ('pas', models.BooleanField(default=True)),
                ('kompetensi_inti', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.KompetensiInti')),
                ('mata_pelajaran_kurikulum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.MataPelajaranKurikulum')),
            ],
            options={
                'verbose_name': 'Kompetensi Dasar',
                'verbose_name_plural': 'Kompetensi Dasar',
                'unique_together': {('mata_pelajaran_kurikulum', 'kompetensi_inti', 'nomor')},
            },
        ),
    ]
