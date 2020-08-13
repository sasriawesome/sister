from django import forms
from django.utils import timezone
from sister.core.enums import Weekday
from sister.modules.presensi.models import (
    PresensiKelas,
    PresensiSiswa
)
from sister.modules.pembelajaran.models import (
    Kelas,
    JadwalPelajaran,
    MataPelajaranKelas,
    JadwalPiketSiswa,
    SiswaKelas,
    RentangNilai,
    )

from tempus_dominus.widgets import DatePicker, TimePicker


class JadwalPelajaranForm(forms.ModelForm):
    class Meta:
        model = JadwalPelajaran
        fields = [
            'kelas',
            'semester',
            'hari',
            'mata_pelajaran',
            'jam_mulai',
            'jam_berakhir',
            'deskripsi'
            ]

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial')
        kelas = initial.get('kelas')
        initial.update({
            'kelas': kelas.id
        })
        super().__init__(*args, **kwargs)
        self.fields['mata_pelajaran'] = forms.ModelChoiceField(
            required=True,
            queryset=MataPelajaranKelas.objects.filter(
                **{'kelas_id': kelas.id}
                ),
            limit_choices_to={'kelas_id': kelas.id}
        )

    kelas = forms.ModelChoiceField(
        required=True,
        queryset=Kelas.objects.all(),
        widget=forms.HiddenInput(attrs={'readonly': True})
    )
    semester = forms.ChoiceField(
        required=True,
        choices=(
            (1, '1'),
            (2, '2'),
        ),
        widget=forms.Select()
    )
    hari = forms.ChoiceField(
        required=True,
        choices=Weekday.CHOICES.value,
        widget=forms.Select()
    )
    jam_mulai = forms.TimeField(
        required=True,
        widget=TimePicker(
            options={
                'enabledHours': [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            },
            attrs={
                'append': 'fa fa-clock',
                'icon_toggle': True,
            })
        )
    jam_berakhir = forms.TimeField(
        required=True,
        widget=TimePicker(
            options={
                'enabledHours': [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            },
            attrs={
                'append': 'fa fa-clock',
                'icon_toggle': True,
            })
        )
    deskripsi = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 5}
            )
        )


class JadwalPiketSiswaForm(forms.ModelForm):
    class Meta:
        model = JadwalPiketSiswa
        fields = ['kelas', 'hari', 'semester', 'siswa_kelas']

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial')
        kelas = initial.get('kelas')
        initial.update({
            'kelas': kelas.id
        })
        super().__init__(*args, **kwargs)
        self.fields['siswa_kelas'] = forms.ModelChoiceField(
            queryset=SiswaKelas.objects.filter(**{'kelas_id': kelas.id}),
            limit_choices_to={'kelas_id': kelas.id}
        )

    kelas = forms.ModelChoiceField(
        queryset=Kelas.objects.all(),
        widget=forms.HiddenInput(attrs={'readonly': True})
    )
    semester = forms.ChoiceField(
        required=True,
        choices=(
            (1, '1'),
            (2, '2'),
        ),
        widget=forms.Select()
    )
    hari = forms.ChoiceField(
        required=True,
        choices=Weekday.CHOICES.value,
        widget=forms.Select()
    )


class RentangNilaiForm(forms.ModelForm):
    class Meta:
        model = RentangNilai
        fields = [
            'kelas', 'predikat', 'nilai_minimum', 'nilai_maximum']

    kelas = forms.ModelChoiceField(
        queryset=Kelas.objects.all(),
        widget=forms.HiddenInput(attrs={'readonly': True})
    )
    predikat = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': True})
        )
    nilai_minimum = forms.IntegerField(
        required=True,
        widget=forms.NumberInput())
    nilai_maximum = forms.IntegerField(
        required=True,
        widget=forms.NumberInput())


class PresensiFilterForm(forms.Form):

    semester = forms.ChoiceField(
        required=False,
        initial='1',
        choices=(
            (1, 'Semester 1'),
            (2, 'Semester 2'),
            ),
        widget=forms.Select()
    )
    bulan = forms.ChoiceField(
        required=False,
        initial=timezone.now().month,
        choices=(
            ('1', 'Januari'),
            ('2', 'Februari'),
            ('3', 'Maret'),
            ('4', 'April'),
            ('5', 'Mei'),
            ('6', 'Juni'),
            ('7', 'Juli'),
            ('8', 'Agustus'),
            ('9', 'September'),
            ('10', 'Oktober'),
            ('11', 'November'),
            ('12', 'Desember'),
            ),
        widget=forms.Select()
    )
    tipe = forms.ChoiceField(
        required=False,
        initial='tabular',
        choices=(
            ('matrix', 'Matrix'),
            ('tabular', 'Tabular'),
            ),
        widget=forms.Select()
    )


class PresensiKelasForm(forms.ModelForm):
    class Meta:
        model = PresensiKelas
        fields = ['kelas', 'semester', 'tanggal', 'aktifitas', 'deskripsi']

    kelas = forms.ModelChoiceField(
        queryset=Kelas.objects.all(),
        widget=forms.HiddenInput(attrs={'readonly': True})
    )
    tanggal = forms.DateField(
            widget=DatePicker(
                options={
                    'useCurrent': True
                },
                attrs={
                    'append': 'fa fa-calendar-alt',
                    'icon_toggle': True,
                }
            )
        )


class PresensiSiswaForm(forms.ModelForm):
    class Meta:
        model = PresensiSiswa
        fields = ['presensi_kelas', 'siswa_kelas', 'status']

    siswa_kelas = forms.ModelChoiceField(
        disabled=True,
        queryset=SiswaKelas.objects.all(),
        widget=forms.Select(attrs={'readonly': True})
    )
