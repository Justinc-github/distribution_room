from django.urls import path
from .views import *

app_name = 'statistics'
urlpatterns = [
    path('', statistics_view, name='statistics_view'),
    path('get-latest-data/', get_latest_data, name='get_latest_data'),
]
