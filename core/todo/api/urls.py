from rest_framework.routers import DefaultRouter
from .views import TaskViewSet,OpenWeatherViewSet
from django.urls import path


app_name = "api"

urlpatterns = [
    path('openweather/', OpenWeatherViewSet.as_view({'get':'list'}), name='openweather'),
]

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")


urlpatterns += router.urls
