import datetime

# =============================================================================
# Constance Settings
# =============================================================================

CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'

CONSTANCE_REDIS_CONNECTION = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 3,
}

CONSTANCE_ADDITIONAL_FIELDS = {
    'char_field': ['django.forms.CharField', {}],
    'date_field': ['django.forms.DateField', {
        'widget': 'django.contrib.admin.widgets.AdminDateWidget'
    }],
    'image_field': ['django.forms.ImageField', {}],
    'email_field': ['django.forms.EmailField', {}]
}

CONSTANCE_CONFIG = {
    # Website Settings
    'SITE_LOGO': ('logo.png', 'Website Logo', 'image_field'),
    'SITE_TITLE': ('My Website', 'Website title', 'char_field'),
    'SITE_SUBTITLE': (
        'Another Awesome Website', 'Website subtitle', 'char_field'
        ),
    'SITE_DESCRIPTION': ('Website about good service', 'Website description'),
    # Company Profile
    'COMPANY_NAME': (
        'My Company',
        'Company or commercial name',
        'char_field'
        ),
    'COMPANY_ADDRESS': (
        'Jl. Ikan Sebelah No.8, Kec. Pesawahan',
        'Company address, street name etc.'
        ),
    'COMPANY_CITY': ('Bandar Lampung', '', 'char_field'),
    'COMPANY_PROVINCE': ('Lampung', '', 'char_field'),
    'COMPANY_COUNTRY': ('Indonesia', '', 'char_field'),
    'COMPANY_POSTALCODE': ('35223', '', 'char_field'),
    'COMPANY_PHONE': ('0721373767', 'Valid phone number', 'char_field'),
    'COMPANY_EMAIL': (
        'mycompany@gmail.com', 'Company email address', 'email_field'),
    # Tahun Anggaran
    'FISCAL_DATE_START': (
        datetime.date(2020, 1, 1), 'Fiscal start date', 'date_field'),
    'FISCAL_DATE_END': (
        datetime.date(2020, 12, 31), 'Fiscal start date', 'date_field'),
    # PDF Settings
    'PDF_MARGIN_TOP': (40, ''),
    'PDF_MARGIN_LEFT': (30, ''),
    'PDF_MARGIN_RIGHT': (30, ''),
    'PDF_MARGIN_BOTTOM': (30, ''),
    'PDF_ORIENTATION': ('portrait', 'Page orientation')
}

CONSTANCE_CONFIG_FIELDSETS = {
    'General Settings': (
        'SITE_LOGO',
        'SITE_TITLE',
        'SITE_SUBTITLE',
        'SITE_DESCRIPTION'
    ),
    'Company Settings': (
        'COMPANY_NAME',
        'COMPANY_ADDRESS',
        'COMPANY_CITY',
        'COMPANY_PROVINCE',
        'COMPANY_COUNTRY',
        'COMPANY_POSTALCODE',
        'COMPANY_PHONE',
        'COMPANY_EMAIL',
    ),
    'Reports Settings': (
        'FISCAL_DATE_START',
        'FISCAL_DATE_END',
        'PDF_MARGIN_TOP',
        'PDF_MARGIN_LEFT',
        'PDF_MARGIN_RIGHT',
        'PDF_MARGIN_BOTTOM',
        'PDF_ORIENTATION'
    ),
}
