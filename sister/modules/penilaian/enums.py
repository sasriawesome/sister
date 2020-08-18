import enum
from sister.core.helpers import snake_to_lower


class JenisPenilaian(enum.Enum):
    TUGAS = 0
    PH = 1
    PTS = 2
    PAS = 3


JENIS_PENILAIAN_CHOICES = [
    (x.value, snake_to_lower(x.name).upper()) for x in JenisPenilaian
]
