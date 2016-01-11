#-*- coding:utf-8 -*-

from datetime import datetime
import pytz

from django.views.generic import View
from django.http import JsonResponse

from account.models import RuntimeHeartBeat, RuntimeMachine

from .runtime import restart_runtime


class RuntimeMachineCheck(View):
    """
    用来检查用户是否在线保证虚机运行
    每次更新数据库心跳表，服务器定时扫描
    """
    def post(self, request):
        account = request.session.get('account', {'id': '1'})

        if account is None:
            return JsonResponse({'status': 'ok', 'data': u'未登录用户'})

        #更新对应的心跳表
        if len(RuntimeHeartBeat.objects.filter(account_id=account['id'])) == 0:
            #之前没记录，新建记录
            runtime_beat = RuntimeHeartBeat(account_id=account['id'],
                                            last_beat=datetime.now(tz=pytz.timezone('Asia/Shanghai')))

            runtime_beat.save()
            return JsonResponse({'status': 'ok', 'data': 'success'})
        runtime_record = RuntimeHeartBeat.objects.get(account_id=account['id'])
        runtime_record.last_beat = datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S") + '+00:00'

        #检查是否宕机，如果宕机，重启虚机
        try:
            runtime_machine = RuntimeMachine.objects.get(account__id=account['id'])
            restart_runtime(runtime_machine.container_id)
        except:
            return JsonResponse({'status': 'error', 'data': 'no runtime found'})

        try:
            runtime_record.save()
            return JsonResponse({'status': 'ok', 'data': 'success'})
        except Exception, e:
            return JsonResponse({'status': 'error', 'data': 'update failed'})