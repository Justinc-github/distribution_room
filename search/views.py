from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from user.models import *


def search_view(request, page):
    word = request.GET.get('word_', '')  # 获取关键字
    if word:
        workers = UserInfo.objects.filter(Q(name__icontains=word) | Q(tel__icontains=word))
    else:
        workers = UserInfo.objects.all()
    return render(request, 'search.html', {
        'workers': workers,
        'word': word
    })


def default_view(request):
    return search_view(request, 1)
