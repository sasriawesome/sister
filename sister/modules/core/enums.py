import enum
from django.utils.translation import ugettext_lazy as _


class MaxLength(enum.Enum):
    SHORT = 128
    MEDIUM = 256
    LONG = 512
    XLONG = 1024
    TEXT = 2048
    RICHTEXT = 10000


class Weekday(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FREEDAY = 4
    SATURDAY = 5
    SUNDAY = 6


WEEKDAY_CHOICES = (
        (0, _('Senin')),
        (1, _('Selasa')),
        (2, _('Rabu')),
        (3, _('Kamis')),
        (4, _('Jumat')),
        (5, _('Sabtu')),
        (6, _('Minggu')),
    )


class ActiveStatus(enum.Enum):
    ACTIVE = 'ACT'
    INACTIVE = 'INC'


ACTIVE_STATUS_CHOICES = (
    (x.value, x.name) for x in ActiveStatus
)


class PrivacyStatus(enum.Enum):
    ME = 1
    USERS = 2
    FRIENDS = 3
    STUDENTS = 4
    TEACHERS = 5
    EMPLOYEES = 6
    MANAGERS = 7
    ANYONE = 99


PRIVACY_STATUS_CHOICES = (
    (x.value, x.name) for x in PrivacyStatus
)


class ProcessStatus(enum.Enum):
    TRASH = 'TRS'
    DRAFT = 'DRF'
    VALID = 'VLD'
    APPROVED = 'APP'
    REJECTED = 'RJC'
    PROCESSED = 'PRS'
    COMPLETE = 'CMP'
    INVOICED = 'INV'
    PENDING = 'PND'
    UNPAID = 'UNP'
    PAID = 'PID'
    CLOSED = 'CLS'
    POSTED = 'PST'


PRIVACY_STATUS_CHOICES = (
        (x.value, x.name) for x in ProcessStatus
    )
