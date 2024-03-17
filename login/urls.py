from django.urls import path

from user.views import user_details
from .views import *

app_name = 'login'
urlpatterns = [
    path('', login, name='login_view'),

    path('user_details/', user_details, name='user_details'),

    path('logout/', logout, name='logout'),
]
