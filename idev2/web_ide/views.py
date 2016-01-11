#-*- coding:utf-8 -*-

import json
from datetime import datetime
import pytz

from django.shortcuts import render
from django.http import JsonResponse

from account.models import Account
from submission.models import Submission

from code_util.util import save_code
from docker_util.tasks import  exec_code


def index(request):
    return render(request, 'web_ide/index.html')


def code_submit(request):
    if request.method == 'POST':
        account_id = '1'
        problem_id = '1'

        code = request.POST.get('code')

        #生成一条submission记录
        submission = Submission()
        submission.account = Account.objects.get(id=account_id)
        submission.submit_time = datetime.now(tz=pytz.UTC)

        code_path = save_code(account_id, problem_id, code)
        submission.code_path = code_path
        submission.problem_id = problem_id

        submission.save()

        #虚机开始运行判题, 异步执行
        exec_code.delay(submission)

        #返回submission的id，用于js轮询状态
        return JsonResponse({'status': 'ok', 'submission': submission.id})