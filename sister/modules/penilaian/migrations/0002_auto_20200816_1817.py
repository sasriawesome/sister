# Generated by Django 3.0.8 on 2020-08-16 18:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sister_kurikulum', '0005_auto_20200814_1917'),
        ('sister_penilaian', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itempenilaianakhirsemester',
            options={'ordering': ['kompetensi__ki', 'kompetensi__kd'], 'verbose_name': 'Penilaian Akhir Semester', 'verbose_name_plural': 'Penilaian Akhir Semester'},
        ),
        migrations.AlterModelOptions(
            name='itempenilaianharian',
            options={'ordering': ['kompetensi__ki', 'kompetensi__kd'], 'verbose_name': 'Penilaian Harian', 'verbose_name_plural': 'Penilaian Harian'},
        ),
        migrations.AlterModelOptions(
            name='itempenilaiantengahsemester',
            options={'ordering': ['kompetensi__ki', 'kompetensi__kd'], 'verbose_name': 'Penilaian Tengah Semester', 'verbose_name_plural': 'Penilaian Tengah Semester'},
        ),
        migrations.AlterModelOptions(
            name='itempenilaiantugas',
            options={'ordering': ['kompetensi__ki', 'kompetensi__kd'], 'verbose_name': 'Penilaian Tugas', 'verbose_name_plural': 'Penilaian Tugas'},
        ),
        migrations.CreateModel(
            name='ItemPenilaian',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('jenis_penilaian', models.IntegerField(choices=[(0, 'TUGAS'), (1, 'PH'), (2, 'PTS'), (3, 'PAS')], default=1, verbose_name='Jenis Penilaian')),
                ('nilai', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('kompetensi', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item_penilaian', to='sister_kurikulum.KompetensiDasar')),
                ('penilaian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nilai', to='sister_penilaian.PenilaianPembelajaran')),
            ],
            options={
                'verbose_name': 'Item Penilaian',
                'verbose_name_plural': 'Item Penilaian',
                'ordering': ['jenis_penilaian', 'kompetensi__ki', 'kompetensi__kd'],
                'unique_together': {('jenis_penilaian', 'penilaian', 'kompetensi')},
            },
        ),
    ]
