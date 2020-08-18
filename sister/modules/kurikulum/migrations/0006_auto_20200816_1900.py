# Generated by Django 3.0.8 on 2020-08-16 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sister_kurikulum', '0005_auto_20200814_1917'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kompetensidasar',
            options={'ordering': ['kurikulum_mapel', 'ki', 'kd'], 'verbose_name': 'Kompetensi Dasar', 'verbose_name_plural': 'Kompetensi Dasar'},
        ),
        migrations.AlterIndexTogether(
            name='kompetensidasar',
            index_together={('kurikulum_mapel', 'ki', 'kd')},
        ),
    ]
