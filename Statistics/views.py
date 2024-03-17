from django.core.serializers import serialize
from django.shortcuts import render
from Statistics.models import value
from django.http import JsonResponse
from Statistics.management.commands.runapscheduler import my_job


def statistics_view(request):
    queryset1 = value.objects.order_by('-id')[:120].values('tem')
    queryset2 = value.objects.order_by('-id')[:120].values('humidity')
    list_data1 = []
    list_data2 = []
    list1 = list(queryset1)
    list2 = list(queryset2)
    for i in range(60):
        data1 = list1[59-i]['tem']
        data2 = list2[59-i]['humidity']
        list_data1.append(data1)
        list_data2.append(data2)
    return render(request, 'statistics.html', {
        'list_data1': list_data1,
        'list_data2': list_data2,
    })


def get_latest_data(request):
    last_data = value.objects.order_by('id').last()
    data = {
        'tem': last_data.tem,
        'humidity': last_data.humidity,
    }
    return JsonResponse(data)
