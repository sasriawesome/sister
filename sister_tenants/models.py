from django.db import models
from django_tenants.models import DomainMixin

from tenant_users.tenants.models import TenantBase


class Sekolah(TenantBase):
    name = models.CharField(max_length=225)
    npsn = models.CharField(max_length=25)
    nss = models.CharField(max_length=25)
    paid_until = models.DateField(auto_now=True)
    trial = models.BooleanField(default=True)

    # default true, schema will be automatically created
    # and synced when it is saved
    auto_create_schema = False

    def check_ownership(self, user_obj):
        return self.owner.id == user_obj.id


class Domain(DomainMixin):
    pass
