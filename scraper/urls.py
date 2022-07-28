from django.urls import path
from . import views

urlpatterns = [
    path('', views.scraper_home, name='scraper_home'),
]
