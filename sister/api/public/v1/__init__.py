import graphene as gp
from .queries import Query
from .mutations import Mutation

schema = gp.Schema(query=Query, mutation=Mutation)
