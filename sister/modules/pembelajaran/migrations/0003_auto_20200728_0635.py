# Generated by Django 3.0.8 on 2020-07-28 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sister_kurikulum', '0001_initial'),
        ('sister_pembelajaran', '0002_auto_20200728_0635'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nilaimatapelajaran',
            unique_together={('nilai_siswa', 'mata_pelajaran')},
        ),
    ]
