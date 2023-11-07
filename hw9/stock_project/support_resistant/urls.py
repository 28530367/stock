from django.urls import path
from . import views

urlpatterns = [
    path('', views.web, name='web'),
    path('run_single/', views.singleSearch, name='run_single'),
]
