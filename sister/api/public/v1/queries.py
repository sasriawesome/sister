from django.contrib.auth import get_user_model
from graphene import relay, ObjectType
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField

from .types import (
    UserNode, SekolahNode, DomainNode
)


class Query(ObjectType):
    user = relay.Node.Field(UserNode)
    user_list = DjangoFilterConnectionField(UserNode)
    sekolah = relay.Node.Field(SekolahNode)
    sekolah_list = DjangoFilterConnectionField(SekolahNode)
    domain = relay.Node.Field(DomainNode)
    domain_list = DjangoFilterConnectionField(DomainNode)

    @login_required
    def resolve_user_list(root, info):
        user = info.context.user
        if user.is_superuser or user.is_staff:
            return get_user_model().objects.all()
        else:
            return get_user_model().objects.filter(pk=user.id)
