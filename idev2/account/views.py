#-*- coding:utf-8 -*-

import re
from hashlib import md5
from datetime import datetime

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render_to_response, render

from .models import Account, RuntimeMachine

from global_util.account_util import send_active_email
from global_util.util import get_current_page, date_to_string, get_total_page

from docker_util.runtime import create_runtime, stop_runtime, start_runtime

from idev2.settings import ITEMS_PER_PAGE


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
            return JsonResponse({'status': 'error', 'data': u'邮箱已被注册'})

        account = Account(name=name, email=email, passwd=md5(passwd).hexdigest(), is_active=0)

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
        return render(request, 'account/login.html')

    def post(self, request):
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')

        try:
            account = Account.objects.get(email=email)
            if account.passwd == md5(passwd).hexdigest():
                if account.is_active == 0:
                    return render(request, 'account/login.html', {'status_info': u'账号还未激活，请激活'})
                else:
                    #登录启动对应虚机
                    try:
                        start_runtime(container_id=RuntimeMachine.objects.get(account=account).container_id)
                    except Exception, e:
                        #TODO 无法启动虚机
                        pass
                    request.session['account'] = {'id': str(account.id),
                                'email': account.email, 'name': account.name}
                    referer_url = request.META.get('HTTP_REFERER')
                    if re.search(r'.*/login/?.*', referer_url):
                        referer_url = '/'
                    else:
                        referer_url = request.META.get('HTTP_REFERER', '/')
                    return HttpResponseRedirect(referer_url)
            else:
                return render(request, 'account/login.html', {'status_info': u'密码不正确'})
        except Exception, e:
            print e
            return render(request, 'account/login.html', {'status_info': u'邮箱不存在'})


class AccountProfileView(View):
    """
    个人页面, 展示个人基本信息，提交数，参加的比赛
    """
    def get(self, request):
        pass

class AccountAdminView(View):
    def get(self, request, account_id):
        pass

    def post(self, request):
        pass


def account_admin_home(request):
    """
    账号管理首页
    :param request:
    :return:
    """
    page = get_current_page(request.GET.get('page'))
    all_account_objs = Account.objects.all().order_by('name')
    total_pages = get_total_page(len(all_account_objs))

    current_account_obj = all_account_objs[(page - 1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]

    account_list = [{'id': account.id, 'name': account.name, 'email': account.email,
                     'is_active': account.is_active, 'active_code': account.active_code}
                    for account in current_account_obj]

    return render(request, 'admin/account_admin_home.html', {'account_list': account_list,
                                                             'page': page,
                                                             'total_pages': total_pages})


def logout(request):
    #停止对应账户的虚机
    if request.session.has_key('account'):
        account = request.session['account']
        try:
            runtime_machine = RuntimeMachine.objects.get(account__id=account['id'])
            stop_runtime(runtime_machine.container_id)
        except:
            #TODO log记录
            pass

        del request.session['account']

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
                    #成功激活后创建虚机
                    create_runtime(account.id)

                    account.save()
                    return render_to_response('account/account_active.html', {'info': u'激活成功，现在可以登录'})
                except Exception, e:
                    return render_to_response('account/account_active.html',
                                              {'info': u'激活失败，请稍后再试或者联系管理人员'})
            else:
                return render_to_response('account/account_active.html', {'info': u'该账号已经激活，请直接登录'})
        except Exception, e:
            return render_to_response('account/account_active.html', {'info': u'激活码错误，请检查一下~'})
    return render_to_response('account/account_active.html', {'info': u"打开方式不对~~"})