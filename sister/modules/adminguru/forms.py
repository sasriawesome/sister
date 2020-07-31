from django import forms
from django.utils.html import mark_safe
from django.forms.models import inlineformset_factory
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget

from sister.modules.pembelajaran.models import *


class PlainTextWidget(forms.Widget):
    def render(self, name, value, attrs, renderer=None):
        if hasattr(self, 'initial'):
            value = self.initial
        return mark_safe(
            (str(value) if value is not None else '-' ) +
            f"<input type='hidden' name='{name}' value='{value}'>"
        )


class SiswaPiketForm(forms.ModelForm):
    class Meta:
        model = ItemPiketKelas
        fields = ['piket_kelas', 'siswa_kelas']

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial')
        piket_kelas = initial.get('piket_kelas')
        initial.update({
            'piket_kelas': piket_kelas.id
        })
        super().__init__(*args, **kwargs)
        self.fields['siswa_kelas'] = forms.ModelChoiceField(
            queryset = SiswaKelas.objects.filter(**{'kelas_id': piket_kelas.kelas.id }),
            limit_choices_to={'kelas_id': piket_kelas.kelas.id }
        )
    
    piket_kelas = forms.ModelChoiceField(
        queryset = PiketKelas.objects.all(),
        widget=forms.HiddenInput(attrs={'readonly':True})
    )


class ItemJadwalPelajaranForm(forms.ModelForm):
    class Meta:
        model = ItemJadwalPelajaran
        fields = ['jadwal_kelas', 'mata_pelajaran', 'jam_mulai', 'jam_berakhir', 'deskripsi']

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial')
        jadwal_kelas = initial.get('jadwal_kelas')
        initial.update({
            'jadwal_kelas': jadwal_kelas.id
        })
        super().__init__(*args, **kwargs)
        self.fields['mata_pelajaran'] = forms.ModelChoiceField(
            required=True,
            queryset = MataPelajaranKelas.objects.filter(**{'kelas_id': jadwal_kelas.kelas.id }),
            limit_choices_to={'kelas_id': jadwal_kelas.kelas.id }
        )
    
    jadwal_kelas = forms.ModelChoiceField(
        required=True,
        queryset = JadwalKelas.objects.all(),
        widget=forms.HiddenInput(attrs={'readonly':True})
    )
    jam_mulai = forms.TimeField( required=True, widget=AdminTimeWidget())
    jam_berakhir = forms.TimeField(required=True, widget=AdminTimeWidget())
    deskripsi = forms.CharField(required=False, widget=forms.Textarea())


class RentangNilaiForm(forms.ModelForm):
    class Meta:
        model = RentangNilai
        fields = ['kelas', 'predikat', 'nilai_minimum', 'nilai_maximum']
    
    kelas = forms.ModelChoiceField(
        queryset = Kelas.objects.all(),
        widget=forms.HiddenInput(attrs={'readonly':True})
    )
    predikat = forms.CharField(widget=forms.TextInput(attrs={'readonly':True}))
    nilai_minimum = forms.IntegerField(
        required=True,
        widget=forms.NumberInput())
    nilai_maximum = forms.IntegerField(
        required=True,
        widget=forms.NumberInput())


class PresensiKelasForm(forms.ModelForm):
    class Meta:
        model = PresensiKelas
        fields = ['kelas', 'semester', 'tanggal']

    kelas = forms.ModelChoiceField(
        queryset = Kelas.objects.all(),
        widget=forms.HiddenInput(attrs={'readonly':True})
    )
    tanggal = forms.DateField(widget=AdminDateWidget())


class PresensiSiswaForm(forms.ModelForm):
    class Meta:
        model = PresensiSiswa
        fields = ['presensi_kelas', 'siswa_kelas', 'status']

    siswa_kelas = forms.ModelChoiceField(
        disabled = True,
        queryset=SiswaKelas.objects.all(),
        widget=forms.Select(attrs={'readonly':True})
    )

PresensiSiswaFormSet = inlineformset_factory(
    PresensiKelas,
    PresensiSiswa, 
    PresensiSiswaForm,
    fields=['siswa_kelas', 'status'],
    extra=0,
    can_delete=False
)