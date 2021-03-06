# Generated by Django 3.1 on 2020-10-16 21:58

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
                ('mata_pelajaran_kurikulum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.matapelajaran')),
            ],
            options={
                'verbose_name': 'Tema',
                'verbose_name_plural': 'Tema',
            },
        ),
        migrations.CreateModel(
            name='KurikulumMataPelajaran',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('kurikulum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mata_pelajaran', to='sister_kurikulum.kurikulum')),
                ('mata_pelajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kurikulum', to='sister_kurikulum.matapelajaran')),
            ],
            options={
                'verbose_name': 'Kurikulum Mata Pelajaran',
                'verbose_name_plural': 'Kurikulum Mata Pelajaran',
                'unique_together': {('kurikulum', 'mata_pelajaran')},
            },
        ),
        migrations.CreateModel(
            name='KompetensiDasar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('ki', models.IntegerField(choices=[(1, 'Sikap Spiritual'), (2, 'Sikap Sosial'), (3, 'Pengetahuan'), (4, 'Keterampilan')], default=3, verbose_name='KI')),
                ('kd', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='KD')),
                ('keyword', models.CharField(help_text="\n            Kata kunci menunjukkan kompetensi\n            Contoh:'Mempraktekkan membaca Surat Al-Fatihah'.\n            ", max_length=255, verbose_name='Keyword')),
                ('deskripsi', models.TextField(blank=True, null=True, verbose_name='Deskripsi')),
                ('kurikulum_mapel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kompetensi_dasar', to='sister_kurikulum.kurikulummatapelajaran')),
            ],
            options={
                'verbose_name': 'Kompetensi Dasar',
                'verbose_name_plural': 'Kompetensi Dasar',
                'ordering': ['kurikulum_mapel', 'ki', 'kd'],
                'unique_together': {('kurikulum_mapel', 'ki', 'kd')},
                'index_together': {('kurikulum_mapel', 'ki', 'kd')},
            },
        ),
    ]
