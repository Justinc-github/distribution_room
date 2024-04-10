import re

from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect

from login import models as login_models
from user import models as user_models
from login.code.code import create_captcha_content
from io import BytesIO


class EnrollForm(forms.ModelForm):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = login_models.user_login
        fields = ['username', 'password', 'name', 'phone']


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={"class": "form-control"}))


def enroll(request):
    form = EnrollForm(request.POST)
    if request.method == "GET":
        form = EnrollForm()
        return render(request, "enroll.html", {"form": form})

    try:
        if request.session['image_code'] != form.data['Captcha']:
            error_message = "验证码错误，请重新输入。"
            return render(request, "login.html", {"error_message": error_message, "form": form})
    except KeyError:
        error_message = "验证码过期，请重新注册。"
        return render(request, "login.html", {"error_message": error_message})

    if form.is_valid():
        form.save()
        return render(request, "login.html", {"form": form})
    return render(request, "enroll.html", {"form": form})


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    user_login = login_models.user_login.objects.filter(username=form.data['username'],
                                                        password=form.data['password']).first()
    try:
        if request.session['image_code'] != form.data['Captcha']:
            error_message = "验证码错误，请重新输入。"
            return render(request, "login.html", {"error_message": error_message})
    except KeyError:
        error_message = "验证码过期，请重新登录。"
        return render(request, "login.html", {"error_message": error_message})
    if form.is_valid():
        # 去数据库校验
        admin_object = login_models.user_login.objects.filter(**form.cleaned_data).first()

        if not admin_object:
            # 添加一个错误提示
            form.add_error("password", "用户名或者密码错误")
            return render(request, "login.html", {"form": form})
        user_details = user_models.UserInfo.objects.filter(tel=user_login.phone)
        # 将生成的字符串存储在cookie和session中
        request.session["info"] = {"tel": user_login.phone, "name": user_login.username,
                                   "password": user_login.password}
        # 时效性为7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return render(request, "user_details.html", {
            "user_details": user_details,
        })
    return render(request, "login.html", {"form": form})


def image_code(request):
    image, text = create_captcha_content()
    request.session["image_code"] = text
    request.session.set_expiry(60)
    stream = BytesIO()
    image.save(stream, "png")
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.clear()
    return redirect("/")

# 发送验证码功能
# def enroll_view(request):
#     receivers = request.GET.get('mailbox')
#     print(receivers)
#     subject = '验证码'
#     content = f'您的注册验证码为:{generate_verification()},有效时间为5分钟,请勿将验证码告诉他人!'
#     enroll = send_email(receivers, subject, content)
#     if enroll:
#         print('邮件发送成功')
#     else:
#         print('邮件发送失败')
#     return render(request, 'enroll.html')
#
#
# def send_email(receivers, subject, content):
#     # 读取环境变量中的敏感信息 发送邮箱账户和对应授权码
#     sender = '1927705375@qq.com'
#     password = 'pgjqjkghmbfabhha'
#     try:
#         # 构造邮件对象
#         msg = MIMEText(content, 'plain', 'utf-8')
#         msg['From'] = formataddr(('管理系统', sender))
#         msg['Subject'] = subject
#
#         # 连接邮箱服务器并登录
#         server = smtplib.SMTP_SSL('smtp.qq.com', 465)
#         server.login(sender, password)
#
#         # 发送邮件
#         for receiver in receivers:
#             msg['To'] = formataddr(('注册用户', receiver))
#             server.sendmail(sender, [receiver], msg.as_string())
#
#         server.quit()
#         return True
#     except Exception:
#         return False
#
#
# def generate_verification():
#     random_list = list(map(lambda x: random.randint(0, 9), [y for y in range(6)]))  # 这里使用map函数跟lambda匿名函数来生成随机的六位数
#     code = "".join('%s' % i for i in random_list)
#     return code
