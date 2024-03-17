from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('<int:page>/', user_view, name='user_view'),

    path('<int:page>/<int:id>/', work_time_, name='work_time_'),

    path('workers/', workers, name='workers'),

    path('user_modify/', user_modify, name='user_modify'),
]
