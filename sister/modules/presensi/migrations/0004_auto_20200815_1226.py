# Generated by Django 3.0.8 on 2020-08-15 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sister_presensi', '0003_auto_20200815_1222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presensikelas',
            old_name='libur',
            new_name='hari_libur',
        ),
    ]