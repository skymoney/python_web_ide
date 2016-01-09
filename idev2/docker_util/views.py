#-*- coding:utf-8 -*-

from django.views.generic import View
from django.http import JsonResponse


class RuntimeMachineCheck(View):
    """
    用来检查用户是否在线保证虚机运行
    每次更新数据库心跳表，服务器定时扫描
    """
    def post(self, request):
        account = request.session.get('account')

        if account is None:
            return JsonResponse({'status': 'ok', 'data': u'未登录用户'})

        #更新对应的心跳表
        return JsonResponse({'status': 'ok', 'data': 'success'})