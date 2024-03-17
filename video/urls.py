from django.urls import path
from .views import *

app_name = 'video'
urlpatterns = [
    path('', webcam_view, name='video'),
]
