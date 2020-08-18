import enum


class PresensiStatus(enum.Enum):
    HADIR = 'H'
    SAKIT = 'S'
    IZIN = 'I'
    ALFA = 'A'
    LIBUR = 'L'


PRESENSI_STATUS_CHOICES = (
        ('H', 'Hadir'),
        ('S', 'Sakit'),
        ('I', 'Izin'),
        ('A', 'Alfa'),
        ('L', 'Libur')
    )