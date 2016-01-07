#-*- coding:utf-8 -*-

import json

from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext

def index(request):
    return render_to_response('web_ide/index.html')


def code_submit(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        return HttpResponse(json.dumps({'status': 'ok'}))