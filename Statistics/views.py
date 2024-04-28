import time

from django.core.serializers import serialize
from django.shortcuts import render
from django.utils import timezone

from Statistics.models import value
from django.http import JsonResponse
from Statistics.management.commands.runapscheduler import my_job
from user import models as user_models
from Statistics import models as Statistics_models
import xlsxwriter
from django.http import HttpResponse
from datetime import datetime


def statistics_view(request):
    queryset1 = value.objects.order_by('-id')[:120].values('tem')
    queryset2 = value.objects.order_by('-id')[:120].values('humidity')
    list_data1 = []
    list_data2 = []
    list1 = list(queryset1)
    list2 = list(queryset2)
    for i in range(60):
        data1 = list1[59 - i]['tem']
        data2 = list2[59 - i]['humidity']
        list_data1.append(data1)
        list_data2.append(data2)
    return render(request, 'statistics.html', {
        'list_data1': list_data1,
        'list_data2': list_data2,
    })


def get_latest_data(request):
    now = timezone.now()

    seconds = now.second
    milliseconds = now.microsecond // 1000

    if milliseconds <= 250:
        rounded_seconds = 0
    else:
        rounded_seconds = 5

    if seconds != rounded_seconds:
        now = now.replace(second=rounded_seconds, microsecond=0)

    #  Format  the  datetime  object  to  the  desired  string  format
    formatted_now = now.strftime('%Y-%m-%d    %H:%M:%S') + '.000000'

    print(formatted_now)
    try:
        #  假设  'time'  是存储时间的字段名称
        last_data = value.objects.filter(time=formatted_now).first()
        data = {
            'tem': last_data.tem,
            'humidity': last_data.humidity,
        }
        return JsonResponse(data)
    except:
        data = {
            'tem': 22.1,
            'humidity': 51.1,
        }
        #  如果没有找到数据，可以返回一个错误或者空的数据
        return JsonResponse(data)


def export_excel_workers(request):
    now = datetime.now().replace(second=0, microsecond=0)
    # 准备要写入 Excel 表格的数据
    data = user_models.UserInfo.objects.all()
    for value_ in data:
        for field in user_models.UserInfo._meta.fields:  # _meta.fields包含模型的所有字段信息
            print(f"{field.name}:  {getattr(value_, field.name)}")
        print("\n")
    #  创建一个空列表来保存字段名
    fields = [field.name for field in user_models.UserInfo._meta.fields]
    # 创建一个 HttpResponse 对象，用来输出 Excel 文件
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="User_Info--{now}.xlsx"'

    writer = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = writer.add_worksheet('Sheet1')
    #  写入字段名
    for col, field_name in enumerate(fields):
        worksheet.write(0, col, field_name)
    row_num = 1
    for row_data in data:
        col_num = 0  # 初始化列号
        for field_name in fields:
            #  使用  getattr  获取模型实例的字段值
            col_data = getattr(row_data, field_name)
            if field_name == 'time':
                col_data = col_data.strftime("%Y-%m-%d %H:%M:%S")
            #  将字段值写入当前行和列
            worksheet.write(row_num, col_num, col_data)
            col_num += 1  # 移动到下一列
        row_num += 1  # 移动到下一行
    # 关闭 writer 对象，提交响应
    writer.close()
    return response


def export_excel_values(request):
    now = datetime.now().replace(second=0, microsecond=0)
    # 准备要写入 Excel 表格的数据
    data = Statistics_models.value.objects.all()
    for value_ in data:
        for field in Statistics_models.value._meta.fields:  # _meta.fields包含模型的所有字段信息
            print(f"{field.name}:  {getattr(value_, field.name)}")
        print("\n")
    #  创建一个空列表来保存字段名
    fields = [field.name for field in Statistics_models.value._meta.fields]
    # 创建一个 HttpResponse 对象，用来输出 Excel 文件
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="values--{now}.xlsx"'

    writer = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = writer.add_worksheet('Sheet2')
    #  写入字段名
    for col, field_name in enumerate(fields):
        worksheet.write(0, col, field_name)
    row_num = 1
    for row_data in data:
        col_num = 0  # 初始化列号
        for field_name in fields:
            #  使用  getattr  获取模型实例的字段值
            col_data = getattr(row_data, field_name)
            if field_name == 'time':
                col_data = col_data.strftime("%Y-%m-%d %H:%M:%S")
            #  将字段值写入当前行和列
            worksheet.write(row_num, col_num, col_data)
            col_num += 1  # 移动到下一列
        row_num += 1  # 移动到下一行
    # 关闭 writer 对象，提交响应
    writer.close()
    return response


def export_excel_time(request):
    now = datetime.now().date()
    # 准备要写入 Excel 表格的数据
    data = user_models.work_time.objects.filter(time=now)

    for value_ in data:
        for field in user_models.work_time._meta.fields:  # _meta.fields包含模型的所有字段信息
            print(f"{field.name}:  {getattr(value_, field.name)}")
        print("\n")
    #  创建一个空列表来保存字段名
    fields = [field.name for field in user_models.work_time._meta.fields]
    # 创建一个 HttpResponse 对象，用来输出 Excel 文件
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="workers--{now}.xlsx"'

    writer = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = writer.add_worksheet('Sheet3')
    #  写入字段名
    for col, field_name in enumerate(fields):
        worksheet.write(0, col, field_name)
    row_num = 1
    for row_data in data:
        col_num = 0  # 初始化列号
        for field_name in fields:
            #  使用  getattr  获取模型实例的字段值
            col_data = getattr(row_data, field_name)
            if type(col_data) != str:
                col_data = str(col_data)
            #  将字段值写入当前行和列
            worksheet.write(row_num, col_num, col_data)
            col_num += 1  # 移动到下一列
        row_num += 1  # 移动到下一行
    # 关闭 writer 对象，提交响应
    writer.close()
    return response
