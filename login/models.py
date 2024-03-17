from django import forms
from django.db import models


class user_login(models.Model):
    username = models.CharField(verbose_name="用户名",  max_length=64)
    password = models.CharField(verbose_name="密码",  max_length=64)
