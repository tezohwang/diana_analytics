from django.urls import path

from . import views

urlpatterns = [
    path('get_stats', views.get_stats, name='get_stats'),
]
