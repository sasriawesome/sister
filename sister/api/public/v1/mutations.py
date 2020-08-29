from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


from graphene import (
    Mutation as MutationBase, ID,
    ObjectType, Field, String, Boolean
)
from graphene.relay.node import from_global_id
from graphql_jwt import ObtainJSONWebToken, Verify, Refresh
from graphql_jwt.decorators import login_required
from tenant_users.tenants.tasks import provision_tenant
from django_tenants.utils import get_tenant_model

from .types import UserNode


class SignUp(MutationBase):
    class Arguments:
        email = String()
        password = String()

    user = Field(lambda: UserNode, required=False)

    @classmethod
    def mutate(cls, root, info, email, password):
        user = None
        validate_email(email)
        validate_password(password)
        UserModel = get_user_model()
        user = UserModel.objects.create_user(
            email=email,
            password=password
        )
        return {'user': user}


class CreateTenant(MutationBase):
    class Arguments:
        tenant_name = String(required=True)
        tenant_slug = String(required=True)
        user_email = String(required=True)
        is_staff = Boolean(default_value=False)

    tenant_domain = String()

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        tenant_domain = provision_tenant(**kwargs)
        return {'tenant_domain': tenant_domain}


class CreateTenantSchema(MutationBase):
    class Arguments:
        tenant_id = ID()

    message = String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, tenant_id):
        node, tenant_pk = from_global_id(tenant_id)
        TenantModel = get_tenant_model()
        try:
            tenant = TenantModel.objects.get(pk=tenant_pk)
            tenant.create_schema(check_if_exists=True)
            message = '%s schema created' % tenant.name
        except Exception as err:
            message = err
        return {
            'message': message
        }


class DeleteTenant(MutationBase):
    class Arguments:
        tenant_id = ID()

    message = String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, tenant_id):
        user = info.context.user
        node, tenant_pk = from_global_id(tenant_id)
        TenantModel = get_tenant_model()
        try:
            tenant = TenantModel.objects.get(pk=tenant_pk)
            if not (tenant.check_ownership(user) or user.is_superuser):
                raise PermissionError("You are not owner or superuser")
            tenant.delete(force_drop=True)
            message = '%s deleted' % tenant.name
        except Exception as err:
            message = err
        return {
            'message': message
        }


class AddTenantUser(MutationBase):
    class Arguments:
        tenant_id = ID(required=True)
        user_id = ID(required=True)
        superuser = Boolean(default_value=False)
        staff = Boolean(default_value=False)

    message = String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, tenant_id, user_id, superuser, staff):
        user = info.context.user
        TenantModel = get_tenant_model()
        UserModel = get_user_model()
        node, tenant_pk = from_global_id(tenant_id)
        node, user_pk = from_global_id(user_id)
        try:
            tenant = TenantModel.objects.get(pk=tenant_pk)
            if not (tenant.check_ownership(user) or user.is_superuser):
                raise PermissionError("You are not owner or superuser")
            user = UserModel.objects.get(pk=user_pk)
            tenant.add_user(user, is_superuser=superuser, is_staff=staff)
            message = "%s is %s user" % (user, tenant)
        except Exception as err:
            message = err
        return {
            'message': message
        }


class RemoveTenantUser(MutationBase):
    class Arguments:
        tenant_id = ID(required=True)
        user_id = ID(required=True)

    message = String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, tenant_id, user_id):
        user = info.context.user
        TenantModel = get_tenant_model()
        UserModel = get_user_model()
        node, tenant_pk = from_global_id(tenant_id)
        node, user_pk = from_global_id(user_id)
        try:
            tenant = TenantModel.objects.get(pk=tenant_pk)
            if not (tenant.check_ownership(user) or user.is_superuser):
                raise PermissionError("You are not owner or superuser")
            user = UserModel.objects.get(pk=user_pk)
            tenant.remove_user(user)
            message = "%s removed from %s" % (user, tenant)
        except Exception as err:
            message = err
        return {
            'message': message
        }


class TransferTenantOwnership(MutationBase):
    class Arguments:
        tenant_id = ID(required=True)
        new_owner_id = ID(required=True)

    message = String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, tenant_id, new_owner_id):
        user = info.context.user
        TenantModel = get_tenant_model()
        UserModel = get_user_model()
        node, tenant_pk = from_global_id(tenant_id)
        node, new_owner_pk = from_global_id(new_owner_id)
        try:
            tenant = TenantModel.objects.get(pk=tenant_pk)
            if not (tenant.check_ownership(user) or user.is_superuser):
                raise PermissionError("You are not owner or superuser")
            new_owner = UserModel.objects.get(pk=new_owner_pk)
            tenant.transfer_ownership(new_owner)
            message = "%s ownership transfered to %s" % (tenant, new_owner)
        except Exception as err:
            message = err
        return {
            'message': message
        }


class Mutation(ObjectType):
    sign_up = SignUp.Field()
    token_obtain = ObtainJSONWebToken.Field()
    token_verify = Verify.Field()
    token_refresh = Refresh.Field()

    tenant_create = CreateTenant.Field()
    tenant_create_schema = CreateTenantSchema.Field()
    tenant_delete = DeleteTenant.Field()
    tenant_add_user = AddTenantUser.Field()
    tenant_remove_user = RemoveTenantUser.Field()
    tenant_transfer_ownership = TransferTenantOwnership.Field()
