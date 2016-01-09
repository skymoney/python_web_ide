#-*- coding:utf-8 -*-

from hashlib import md5
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.shortcuts import render_to_response

from .models import Account

from global_util.account_util import send_active_email

class AccountRegisterView(View):
    """
    注册View，包括get和post方法
    """
    def get(self, request):
        return render_to_response('account/register.html')

    def post(self, request):
        """
        注册用户并发送激活邮件，激活后创建虚机
        :param request: {'name': '', 'email': '', 'passwd': ''}
        :return:
        """
        name = request.POST.get('name')
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')

        #检查是否重复
        if len(Account.objects.filter(email=email)) > 0:
            return JsonResponse({'status': 'error', 'data': u'邮箱已经被注册'})

        account = Account(name=name, email=email, passwd=passwd, is_active=0)

        #生成激活码
        active_code = md5(str(email) + datetime.now().strftime("%Y%m%d%H%M%S")).hexdigest()
        account.active_code = active_code

        try:
            account.save()
            #发送激活邮件
            if send_active_email(email, active_code):
                return JsonResponse({'status': 'ok', 'data': u'注册成功，请激活邮件'})
            else:
                return JsonResponse({'status': 'error', 'data': u'发送激活邮件失败，请稍后点击重新发送'})
        except:
            return JsonResponse({'status': 'error', 'data': u'注册账号失败'})


class AccountLoginView(View):
    """
    用户登录，包括get和post
    """
    def get(self, request):
        return render_to_response('account/login.html')

    def post(self, request):
        pass


def logout(request):
    #停止对应账户的虚机

    del request.session['account']


def resend_active_email(request):
    """
    重新发送激活邮件
    :param request:
    :return:
    """
    pass


def active_account(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        try:
            account = Account.objects.get(active_code=code)

            if account.is_active == 0:
                account.is_active = 1
                try:
                    account.save()

                    #成功激活后创建虚机
                    return render_to_response('account/account_active.html', {'info': u'激活成功，现在可以登录'})
                except:
                    return render_to_response('account/account_active.html',
                                              {'info': u'激活失败，请稍后再试或者联系管理人员'})
            else:
                return render_to_response('account/account_active.html', {'info': u'该账号已经激活，请直接登录'})
        except:
            return render_to_response('account/account_active.html', {'info': u'激活码错误，请检查一下~'})
    return render_to_response('account/account_active.html', {'info': u"打开方式不对~~"})