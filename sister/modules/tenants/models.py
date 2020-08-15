from django.db import models
# from tenant_users.tenants.models import TenantBase
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class Sekolah(models.Model):
    class Meta:
        verbose_name = 'Sekolah'
        verbose_name_plural = 'Sekolah'

    npsn = models.CharField(max_length=25)
    nss = models.CharField(max_length=25)
    nama_sekolah = models.CharField(max_length=225)

    def __str__(self):
        return self.nama_sekolah


class Domain(DomainMixin):
    pass

