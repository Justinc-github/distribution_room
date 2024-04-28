from django.urls import path
from .views import *

app_name = 'statistics'
urlpatterns = [
    path('', statistics_view, name='statistics_view'),

    path('get-latest-data/', get_latest_data, name='get_latest_data'),

    path('export_excel_workers/',  export_excel_workers,  name='export_excel_workers'),

    path('export_excel_values/',  export_excel_values,  name='export_excel_values'),

    path('export_excel_time/',  export_excel_time,  name='export_excel_time'),
]
