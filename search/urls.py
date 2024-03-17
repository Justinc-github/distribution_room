from django.urls import path
from .views import *

app_name = 'search'
urlpatterns = [
    path('<int:page>/', search_view, name='search_view'),

    path('', default_view, name='default_view')
]


