from rest_framework.response import Response
from todo.models import Task
from .serializers import TaskSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# class TodoListView(viewsets.ModelViewSet)
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = TaskSerializer(queryset, many=True)
#         return Response(serializer.data)


#     def get_queryset(self, *args, **kwargs):
#         return(
#             super()
#             .get_queryset(*args, **kwargs)
#             .filter(user=self.request.user)
#         )

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class TodoDetailApiView(viewsets.ModelViewSet):
#     serializer_class = TaskSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'todo_id'


#     def get_object(self, queryset=None):
#         obj = Task.objects.get(pk=self.kwargs['todo_id'])
#         return obj

#     def delete(self, request, *args, **kwargs):
#         object = self.get_object()
#         object.delete()
#         return Response({'detail': 'successfully removed'})

#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)


#     def post(self, request, *args, **kwargs):
#         object = self.get_object()
#         serializer = TaskSerializer(data=request.data, instance=object, many=False)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["complete"]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self, *args, **kwargs):

        return super().get_queryset(*args, **kwargs).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class OpenWeatherViewSet(viewsets.ViewSet):

    @method_decorator(cache_page(60 * 20))
    def list(self, request, *args, **kwargs):
        get_info = requests.get('https://api.openweathermap.org/data/2.5/weather?q=Tehran&lang=fa&units=metric&appid=971219b8655bd2161e8bba8c6fb9e569').json()
        return Response(get_info)