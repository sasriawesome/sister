import graphene as gp
from .queries import Query


schema = gp.Schema(query=Query)

__all__ = ['schema']
