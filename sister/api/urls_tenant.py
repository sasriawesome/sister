from django.urls import path
from graphene_django.views import GraphQLView
from .tenant.v1 import schema as schema_v1

urlpatterns = [
    path(
        'v1/',
        GraphQLView.as_view(schema=schema_v1, graphiql=True),
        name='api_url_v1'
    ),
]
