from django.shortcuts import Http404
from django.views.generic import TemplateView
from graphene import Schema


class GrapheneView(TemplateView):
    operation = None
    schema = None
    query = None

    def get_variables(self):
        return self.kwargs

    def get_schema(self):
        if not self.schema:
            raise NotImplementedError('Schema property not set!')
        if not isinstance(self.schema, Schema):
            raise NotImplementedError('Schema property must be'
                                      'subclass of graphene.Schema!')
        return self.schema

    def get_query(self):
        return self.query

    def get_operation(self):
        return self.operation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({})
        return context

    def execute(self, query=None):
        schema = self.get_schema()
        context = {
            'request': self.request,
        }
        exec_params = {
            'variables': self.get_variables(),
            'context': context
        }
        results = schema.execute(self.get_query(), **exec_params)
        data = getattr(results, 'data', None)
        errors = getattr(results, 'errors', None)
        return data, errors

    def get(self, *args, **kwargs):
        self.kwargs = kwargs
        data, errors = self.execute()
        if errors or data[self.operation] is None:
            raise Http404('%s not found!' % self.get_operation().title())
        context = self.get_context_data(data=data, errors=errors, **kwargs)
        return self.render_to_response_results(context)


class KurikulumListView(GrapheneView):
    template_name = 'kelas.html'
    query = """
    {
        kurikulumList {
            edges {
                node {
                    id
                    tahun
                    tingkat
                }
            }
        }
    }
    """


class KurikulumView(GrapheneView):
    template_name = 'kelas.html'
    query = """
        query getKurikulum($id: ID!){
            kurikulum(id:$id) {
                id
                tahun
                tingkat
            }
        }
    """
