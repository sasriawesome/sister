# Generated by Django 3.0.8 on 2020-08-14 18:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sister_kurikulum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kompetensidasar',
            options={'verbose_name': 'Kompetensi Dasar', 'verbose_name_plural': 'Kompetensi Dasar'},
        ),
        migrations.CreateModel(
            name='KurikulumMataPelajaran',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('kurikulum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.Kurikulum')),
                ('mata_pelajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kompetensi', to='sister_kurikulum.MataPelajaran')),
            ],
            options={
                'verbose_name': 'Kurikulum Mata Pelajaran',
                'verbose_name_plural': 'Kurikulum Mata Pelajaran',
            },
        ),
        migrations.AddField(
            model_name='kompetensidasar',
            name='kurikulum_mapel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sister_kurikulum.KurikulumMataPelajaran'),
        ),
        migrations.AlterUniqueTogether(
            name='kompetensidasar',
            unique_together={('kurikulum_mapel', 'ki', 'kd')},
        ),
        migrations.RemoveField(
            model_name='kompetensidasar',
            name='kurikulum',
        ),
        migrations.RemoveField(
            model_name='kompetensidasar',
            name='mata_pelajaran',
        ),
    ]