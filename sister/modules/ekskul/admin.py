from sister.admin.admin import ModelAdmin


class PenilaianEkstraKurikulerAdmin(ModelAdmin):
    fields = ['siswa', 'ekskul', 'semester', 'nilai']
    list_display = [
        'siswa',
        'ekskul',
        'semester',
        'nilai',
        # 'predikat'
        ]
