from django.shortcuts import render, redirect
from login.views import EnrollForm
from user import models as user_models
from django.core.paginator import Paginator
import datetime
from login import models as login_models


def user_view(request, page):
    users = user_models.UserInfo.objects.all()
    work_time = user_models.work_time.objects.all()
    dynamics = users.order_by('age')
    page_num = 10
    paginator = Paginator(dynamics, page_num)
    dynamics = paginator.get_page(page)
    total_page = paginator.count
    page_list = [i for i in range(page - 2, page + 3) if 1 <= i <= paginator.num_pages]
    return render(request, 'user_list.html', {
        'users': users,
        'work_time': work_time,
        'dynamics': dynamics,
        'page_list': page_list,
        'total_page': total_page,
        'page': page,
        'paginator': paginator
    })


def default_user_view(request):
    return user_view(request, 1)


def work_time_(request, page, id):
    user = user_models.UserInfo.objects.filter(id=id)
    username = user[0]
    work_time = user_models.work_time.objects.filter(username_id=id).order_by('time')[:10]
    dynamics = user.order_by('work_time')
    page_num = 10
    paginator = Paginator(dynamics, page_num)
    dynamics = paginator.get_page(page)
    total_page = page_num * (page - 1)
    page_list = [i for i in range(page - 2, page + 3) if 1 <= i <= paginator.num_pages]
    return render(request, 'work_time.html', {
        'work_time': work_time,
        'dynamics': dynamics,
        'page_list': page_list,
        'total_page': total_page,
        'page': page,
        'id': id,
        'username': username
    })


def workers(request):
    items = []
    workers = []
    time = datetime.date.today()
    work_time = user_models.work_time.objects.filter(time=time)
    for item in work_time:
        items.append(item.username_id)
    for i in items:
        worker = user_models.UserInfo.objects.filter(id=i)
        workers.append(worker[0])
    return render(request, 'workers.html', {
        'workers': workers,
    })


def user_details(request):
    user_info_from_session = request.session.get("info", {})
    user_tel = user_info_from_session.get("tel")
    user_details = user_models.UserInfo.objects.filter(tel=user_tel)
    return render(request, 'user_details.html', {
        "user_details": user_details,
    })


def user_modify(request):
    user_info_from_session = request.session.get("info", {})
    user_tel = user_info_from_session.get("tel")
    user_mine = login_models.user_login.objects.filter(phone=user_tel).values()

    if request.method == 'POST':
        form = EnrollForm(request.POST)
        user_instance = login_models.user_login.objects.get(phone=user_tel)
        try:
            new_username = form.data['title'][0]
            new_password = form.data['title'][0]
        except KeyError:
            return render(request, 'error.html')
        user_mine[0]['username'] = new_username
        user_mine[0]['password'] = new_password
        user_instance.username = new_username
        user_instance.password = new_password
        user_instance.save()
        request.session.clear()
        return redirect("/")
    return render(request, 'user_modify.html', {"user_mine": user_mine})


