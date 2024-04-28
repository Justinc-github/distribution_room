from django.urls import path
from .views import *

app_name = 'video'
urlpatterns = [
    path('', video_feed, name='video_feed'),
]