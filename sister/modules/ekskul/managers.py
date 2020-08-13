from django.db import models
from django.utils import timezone


class JadwalEkskulManager(models.Manager):
    pass

    def get_by_kelas(self, kelas, current_day=True):
        filters = {
                'jadwal_kelas__kelas': kelas.id,
            }
        if current_day:
            filters['hari'] = timezone.now().weekday()
        return self.filter(**filters).annotate(
                kelas=models.F('jadwal_kelas__kelas'),
                hari=models.F('jadwal_kelas__hari')
            )
