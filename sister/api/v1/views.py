from django.views import View
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

# from sister.modules.todo.models import Work
# from .serializers import WorkSerializer

# class RootView(View):
#     def get(self, request):
#         return JsonResponse(data={'message': 'Welcome to Simpellab V1'})


# class WorkViewSet(ModelViewSet):
#     queryset = Work.objects.all()
#     serializer_class = WorkSerializer

#     @action(methods=['get'], detail=False, url_path='notify')
#     def notify(self, request):
#         Work.send_email("Rizki Sasri Dwitama", "Hello")
#         return JsonResponse({'message': "Rizki Sasri Dwitama"})