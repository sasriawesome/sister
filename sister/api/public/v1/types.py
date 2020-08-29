
from graphene import relay
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from tenant_users.permissions.models import UserTenantPermissions

from sister.tenants.models import Sekolah, Domain


class UserTenantPermissionNode(DjangoObjectType):
    class Meta:
        model = UserTenantPermissions
        interfaces = (relay.Node,)


class PermissionNode(DjangoObjectType):
    class Meta:
        model = Permission
        interfaces = (relay.Node,)


class Group(DjangoObjectType):
    class Meta:
        model = Group
        interfaces = (relay.Node,)


class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        filter_fields = ['is_active']
        exclude = ['password', 'sekolah_set']
        interfaces = (relay.Node,)


class SekolahNode(DjangoObjectType):
    class Meta:
        model = Sekolah
        filter_fields = '__all__'
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class DomainNode(DjangoObjectType):
    class Meta:
        model = Domain
        filter_fields = '__all__'
        interfaces = (relay.Node,)
