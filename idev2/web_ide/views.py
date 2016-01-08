#-*- coding:utf-8 -*-

import json
from datetime import datetime
import pytz

from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext

from account.models import Account
from submission.models import Submission

from code_util.util import save_code
from docker_util.runtime import exec_code

def index(request):
    return render_to_response('web_ide/index.html')


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
        submission.problem_id = 1

        submission.save()

        #虚机开始运行判题, 异步执行
        if exec_code(submission) != 0:
            print 'runtime error'

        return HttpResponse(json.dumps({'status': 'ok'}))