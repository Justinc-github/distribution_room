from django.db import models


class value(models.Model):
    tem = models.FloatField(verbose_name="温度")
    humidity = models.FloatField(verbose_name="湿度")
    time = models.DateTimeField(verbose_name="时间")
