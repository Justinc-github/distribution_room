from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from login import models as login_models
from user import models as user_models
from login.code.code import create_captcha_content
from io import BytesIO

import random
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class EnrollForm(forms.ModelForm):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.CharField(label="邮箱", widget=forms.TextInput(attrs={"class": "form-control"}))
    name = forms.CharField(label="姓名", widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="电话", widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = login_models.user_login
        fields = ['username', 'password', 'name', 'phone', 'email']


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class retrieve(forms.Form):
    email_box = forms.CharField(label="邮箱", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="新密码", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class information_modify(forms.Form):
    username = forms.CharField(label="姓名", widget=forms.TextInput(attrs={"class": "form-control"}))
    age = forms.IntegerField(label="年龄", widget=forms.TextInput(attrs={"class": "form-control"}))


def enroll(request):
    form = EnrollForm(request.POST)
    if request.method == "GET":
        form = EnrollForm()
        return render(request, "enroll.html", {"form": form})
    try:
        if request.session['image_code'] != form.data['Captcha']:
            error_message = "验证码或密码错误，请重新输入。"
            return render(request, "enroll.html", {"error_message": error_message, "form": form})
    except KeyError:
        error_message = "验证码过期，请重新注册。"
        return render(request, "enroll.html", {"error_message": error_message})

    for phone in user_models.UserInfo.objects.values_list('tel', flat=True):
        if form.data['phone'] == phone:
            error_message = "该账号手机号已注册,请登录"
            return render(request, "login.html", {"error_message": error_message})

    for username in login_models.user_login.objects.values_list('username', flat=True):
        if form.data['username'] == username:
            error_message = "该账号用户名已注册,请登录"
            return render(request, "login.html", {"error_message": error_message})
    try:
        for email in user_models.UserInfo.objects.values_list('email', flat=True):
            if form.data['email'] == email:
                error_message = "该账号邮箱已注册,请登录"
                return render(request, "login.html", {"error_message": error_message})
            else:
                print(form.is_valid())
                if form.is_valid():
                    form.save()
                    return render(request, "login.html", {"form": form})
    except:
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
        user_details = user_models.UserInfo.objects.filter(email=user_login.email)
        # 将生成的字符串存储在cookie和session中
        request.session["info"] = {"tel": user_login.phone, "name": user_login.username,
                                   "password": user_login.password, "user": user_login.name}
        # 时效性为7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return render(request, "user_details.html", {
            "user_details": user_details,
            "user": user_login.name,
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


def retrieve_view(request):
    try:
        if request.POST['password1'] == request.POST['password2']:
            try:
                if request.session["code"]:
                    error_message = '验证码已发送，请输入验证码!'
                    email_ = request.POST['email']
                    if request.method == 'POST':
                        user_instance = login_models.user_login.objects.filter(email=email_)
                        print(user_instance[0].password)
                        if request.POST['code']:
                            try:
                                code = request.session["code"]['code']
                                code_ = request.POST['code']
                                if code_ == code:
                                    new_password = request.POST['password1']
                                    user_instance[0].password = new_password
                                    user_instance[0].save()
                                    request.session.clear()
                                    return redirect("/")
                                else:
                                    error_message = '验证码错误，请重新输入验证码!'
                                    print(request.session["code"])
                                    return render(request, 'retrieve.html', {
                                        'error_message': error_message,
                                        'email': request.POST['email'],
                                        'password1': request.POST['password1'],
                                        'password2': request.POST['password2'],
                                    })
                            except:
                                error_message = '验证码过期，请重新输入验证码!'
                                retrieve_code(request, [request.POST['email']])
                                return render(request, 'retrieve.html', {
                                    'error_message': error_message,
                                    'email': request.POST['email'],
                                    'password1': request.POST['password1'],
                                    'password2': request.POST['password2'],
                                })
                        else:
                            error_message = '验证码不能为空!'
                            return render(request, 'retrieve.html', {
                                'error_message': error_message,
                                'email': request.POST['email'],
                                'password1': request.POST['password1'],
                                'password2': request.POST['password2'],
                            })
                    return render(request, 'retrieve.html', {
                        'error_message': error_message,
                        'email': request.POST['email'],
                        'password1': request.POST['password1'],
                        'password2': request.POST['password2'],
                    })
                else:
                    error_message = '验证码错误，请输入验证码!'
                    retrieve_code(request, [request.POST['email']])
                    return render(request, 'retrieve.html', {
                        'error_message': error_message,
                        'email': request.POST['email'],
                        'password1': request.POST['password1'],
                        'password2': request.POST['password2'],
                    })
            except:
                retrieve_code(request, [request.POST['email']])
                error_message = '验证码发送成功，请重新输入验证码!'
                return render(request, 'retrieve.html', {
                    'error_message': error_message,
                    'email': request.POST['email'],
                    'password1': request.POST['password1'],
                    'password2': request.POST['password2'],
                })
        else:
            error_message = '两次输入的密码不一致，请重新输入!'
            return render(request, 'retrieve.html', {
                'error_message': error_message,
                'email': request.POST['email'],
                'password1': request.POST['password1'],
                'password2': request.POST['password2'],
            })
    except:
        return render(request, 'retrieve.html')


def generate_verification():
    return "".join(str(random.randint(0, 9)) for _ in range(6))


def send_email(receivers, subject, content):
    sender = '1927705375@qq.com'
    password = 'sfjqdvsfmybdchah'
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(('管理系统', sender))
        msg['Subject'] = subject
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(sender, password)
        for receiver in receivers:
            msg['To'] = formataddr(('注册用户', receiver))
            server.sendmail(sender, [receiver], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print('邮件发送失败，错误信息：', str(e))
        return False


def retrieve_code(request, receivers):
    subject = '验证码'
    code = generate_verification()
    content = f'您的注册验证码为:{code},有效时间为5分钟,请勿将验证码告诉他人!'
    send_email(receivers, subject, content)
    # 将生成的字符串存储在cookie和session中
    request.session["code"] = {"code": code}
    # 时效性为5分钟
    request.session.set_expiry(60 * 5)
    return HttpResponse(code)


def retrieve_return(request):
    return render(request, 'login.html')
