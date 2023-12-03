from django.urls import path
from . import views

urlpatterns = [
    path('', views.web, name='web'),
    path('add_track/', views.addTrack, name='add_track'),
    path('get_track_list/', views.getTrackList, name='get_track_list'),
    path('remove_track/', views.removeTrack, name='remove_track')
]