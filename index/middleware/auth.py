from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from user import models as user_models
from login import models as login_models


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 登录页面无需校验
        if request.path_info in ["/login/", "", "/login/enroll/", '/login/code/', '/login/retrieve/', '/login/retrieve_code/']:
            return

        # 读取当前用户访问的session信息，如果读取到，说明已登录
        info_dict = request.session.get("info")
        try:

            if info_dict:
                request.unicom_username = user_models.UserInfo.objects.filter(tel=info_dict['tel'])
                request.login_info = login_models.user_login.objects.filter(phone=info_dict['tel']).first()
                return
            else:
                # 如果没有登录，则重定向到登录页面
                return redirect("/login/")
        except:
            return redirect("/login/")

    def process_response(self, request, response):
        return response
