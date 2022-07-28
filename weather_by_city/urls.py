from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_by_city, name='weather_by_city'),
]
