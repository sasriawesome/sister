# Generated by Django 3.0.8 on 2020-08-14 18:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sister_ruang', '0001_initial'),
        ('sister_kurikulum', '0001_initial'),
        ('sister_personal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kelas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('nama_kelas', models.CharField(max_length=225)),
                ('kelas', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], default=1)),
                ('semester', models.IntegerField(choices=[(1, 1), (2, 2)], default=1, help_text='Tampilkan informasi kelas berdasarkan semester')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('AKTIF', 'Aktif'), ('SELESAI', 'Selesai')], default='PENDING', help_text='Tandai kelas sebagai: Pending, Aktif atau Selesai', max_length=10)),
                ('guru_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kelas', to='sister_personal.Guru')),
                ('kurikulum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kelas_belajar', to='sister_kurikulum.Kurikulum')),
                ('ruang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ruang', to='sister_ruang.Ruang')),
                ('tahun_ajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.TahunAjaran')),
            ],
            options={
                'verbose_name': 'Kelas',
                'verbose_name_plural': 'Kelas',
                'ordering': ['kelas', 'tahun_ajaran__tahun_mulai'],
            },
        ),
        migrations.CreateModel(
            name='SiswaKelas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('no_urut', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('status', models.IntegerField(choices=[(1, 'Baru'), (2, 'Tinggal Kelas'), (99, 'Lainnya')], default=1)),
                ('status_lain', models.CharField(blank=True, max_length=56, null=True)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='siswa', to='sister_pembelajaran.Kelas')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kelas', to='sister_personal.Siswa')),
            ],
            options={
                'verbose_name': 'Siswa Kelas',
                'verbose_name_plural': 'Siswa Kelas',
                'ordering': ['no_urut'],
                'unique_together': {('siswa', 'kelas')},
            },
        ),
        migrations.CreateModel(
            name='MataPelajaranKelas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('metode_penilaian', models.IntegerField(choices=[(0, 'Metode Rata Rata'), (1, 'Metode Terbobot')], default=0)),
                ('kkm', models.PositiveIntegerField(default=65, help_text='Kriteria Ketuntasan Minimal', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('bobot_tugas', models.PositiveIntegerField(default=10, help_text='Tugas dan Pekerjaan Rumah', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('bobot_ph', models.PositiveIntegerField(default=20, help_text='Penilaian Harian', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('bobot_pts', models.PositiveIntegerField(default=30, help_text='Penilaian Tengah Semester', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('bobot_pas', models.PositiveIntegerField(default=40, help_text='Penilaian Akhir Semester', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mata_pelajaran_kelas', to='sister_personal.Guru')),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mata_pelajaran_kelas', to='sister_pembelajaran.Kelas')),
                ('mata_pelajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mata_pelajaran_kelas', to='sister_kurikulum.MataPelajaran')),
            ],
            options={
                'verbose_name': 'Guru Mata Pelajaran',
                'verbose_name_plural': 'Guru Mata Pelajaran',
                'unique_together': {('kelas', 'mata_pelajaran')},
            },
        ),
        migrations.CreateModel(
            name='RentangNilai',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('nilai_minimum', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('nilai_maximum', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('predikat', models.CharField(choices=[('A', 'sangat baik'), ('B', 'baik'), ('C', 'cukup baik'), ('D', 'kurang baik'), ('E', 'sangat kurang')], default='A', max_length=1)),
                ('aksi', models.CharField(choices=[('pertahankan', 'pertahankan'), ('tingkatkan', 'tingkatkan'), ('perlu_bimbingan', 'perlu bimbingan')], default='tingkatkan', max_length=125)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentang_nilai', to='sister_pembelajaran.Kelas')),
            ],
            options={
                'verbose_name': 'Rentang Nilai',
                'verbose_name_plural': 'Rentang Nilai',
                'unique_together': {('kelas', 'predikat')},
            },
        ),
        migrations.CreateModel(
            name='KesehatanSiswa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('semester', models.IntegerField(choices=[(1, 1), (2, 2)], default=1)),
                ('berat_badan', models.IntegerField(default=15, validators=[django.core.validators.MinValueValidator(15), django.core.validators.MaxValueValidator(100)])),
                ('tinggi_badan', models.IntegerField(default=50, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(200)])),
                ('siswa_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kesehatan_siswa', to='sister_pembelajaran.SiswaKelas')),
            ],
            options={
                'verbose_name': 'Kesehatan Siswa',
                'verbose_name_plural': 'Kesehatan Siswa',
                'unique_together': {('siswa_kelas', 'semester')},
            },
        ),
        migrations.CreateModel(
            name='JadwalPiketSiswa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('semester', models.IntegerField(choices=[(1, 1), (2, 2)], default=1)),
                ('hari', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Freeday'), (5, 'Saturday'), (6, 'Sunday')], default=0)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='piket', to='sister_pembelajaran.Kelas')),
                ('siswa_kelas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='piket_kelas', to='sister_pembelajaran.SiswaKelas')),
            ],
            options={
                'verbose_name': 'Jadwal Piket Siswa',
                'verbose_name_plural': 'Jadwal Piket Siswa',
                'unique_together': {('kelas', 'semester', 'hari', 'siswa_kelas')},
            },
        ),
        migrations.CreateModel(
            name='JadwalPelajaran',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('semester', models.IntegerField(choices=[(1, 1), (2, 2)], default=1)),
                ('hari', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Freeday'), (5, 'Saturday'), (6, 'Sunday')], default=0)),
                ('jam_mulai', models.TimeField(default=django.utils.timezone.now)),
                ('jam_berakhir', models.TimeField(default=django.utils.timezone.now)),
                ('deskripsi', models.CharField(blank=True, max_length=225, null=True)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jadwal_pelajaran', to='sister_pembelajaran.Kelas')),
                ('mata_pelajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jadwal_pelajaran', to='sister_pembelajaran.MataPelajaranKelas')),
            ],
            options={
                'verbose_name': 'Jadwal Kelas',
                'verbose_name_plural': 'Jadwal Kelas',
                'unique_together': {('kelas', 'semester', 'hari', 'mata_pelajaran')},
            },
        ),
        migrations.CreateModel(
            name='CatatanSiswa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('semester', models.IntegerField(choices=[(1, 1), (2, 2)], default=1)),
                ('deskripsi', models.TextField()),
                ('siswa_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catatan_siswa', to='sister_pembelajaran.SiswaKelas')),
            ],
            options={
                'verbose_name': 'Catatan Siswa',
                'verbose_name_plural': 'Catatan Siswa',
                'unique_together': {('siswa_kelas', 'semester')},
            },
        ),
    ]
