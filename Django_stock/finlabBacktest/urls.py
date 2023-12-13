from django.urls import path
from . import views

urlpatterns = [
    path('finlabBacktest/', views.finlabBacktest),
    path('ajax_finlabBacktest/', views.ajax_finlabBacktest)
]