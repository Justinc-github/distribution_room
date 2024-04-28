from django.urls import path

from user.views import user_details
from .views import *

app_name = 'login'
urlpatterns = [
    path('', login, name='login_view'),

    path('enroll/', enroll, name='enroll'),

    path('user_details/', user_details, name='user_details'),

    path('logout/', logout, name='logout'),

    path('code/', image_code, name="image_code"),

    path('retrieve/', retrieve_view, name="retrieve_view"),

    path('', retrieve_return, name="retrieve_return"),
]
