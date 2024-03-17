from django.urls import path


from .views import *

app_name = 'index'
urlpatterns = [
    path('', index_view, name='index_view'),

]
