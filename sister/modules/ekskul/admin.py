from django.contrib.admin import ModelAdmin
from sister.contrib.admin import admin_site

from .models import (
    EkstraKurikuler,
    TahunAngkatan,
    PesertaEkstraKurikuler,
    PenilaianEkstraKurikuler,
    JadwalEkstraKurikuler
)

admin_site.register(EkstraKurikuler, ModelAdmin)
admin_site.register(TahunAngkatan, ModelAdmin)
admin_site.register(PesertaEkstraKurikuler, ModelAdmin)
admin_site.register(PenilaianEkstraKurikuler, ModelAdmin)
admin_site.register(JadwalEkstraKurikuler, ModelAdmin)
