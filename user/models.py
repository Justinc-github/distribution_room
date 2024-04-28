from django.db import models


class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    salary = models.DecimalField(verbose_name="收入", max_digits=10, decimal_places=2, default=0)
    tel = models.CharField(verbose_name="电话", max_length=32)
    create_time = models.DateField(verbose_name="入职时间")
    gender_choice = (
        (0, "男"),
        (1, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)
    email = models.CharField(verbose_name="邮箱", max_length=20)

    def __str__(self):
        return self.name


class work_time(models.Model):
    username = models.ForeignKey(verbose_name="值班人员", to=UserInfo, on_delete=models.CASCADE)
    time = models.DateField(verbose_name="值班时间", max_length=64)

    def __str__(self):
        return self.time
