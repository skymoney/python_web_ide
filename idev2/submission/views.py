#-*- coding:utf-8 -*-

import pytz
import math

from django.views.generic import View
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from submission.models import Submission

from global_util.submission_util import submission_auth_check

from idev2.settings import ITEMS_PER_PAGE


class SubmissionQueryView(View):
    @submission_auth_check
    def post(self, request):
        """
        提供提交状态查询接口
        :param request: {'submission_id': ''}
        :return: {'status': '', 'data': 'running/accepted/fail', 'info': '', score: ''}
        """
        submission_id = request.POST.get('submission_id')

        try:
            submission = Submission.objects.get(id=submission_id)
            if submission.accepted_info:
                score = submission.accepted_info
            else:
                score = '--'
            return JsonResponse({'status': 'ok', 'data': submission.status, 'score': score, 'info': submission.info})
        except:
            return JsonResponse({'status': 'error', 'data': u'提交记录不存在'})


class MySubmissionView(View):
    def get(self, request, problem_id=None):
        """
        查看 我的提交, 包括全部或指定习题的提交
        :param request:
        :return:
        """
        try:
            page = int(request.GET.get('page', 1))
        except:
            page = 1
        filtered_subs = Submission.objects

        if problem_id:
            filtered_subs = filtered_subs.filter(problem_id=problem_id)
        current_subs = filtered_subs.all().order_by('-submit_time')[(page-1) * ITEMS_PER_PAGE: (page) * ITEMS_PER_PAGE]
        total_pages = int(math.ceil(len(filtered_subs.all())*1.0 /ITEMS_PER_PAGE)) \
            if len(filtered_subs.all()) > 0 else 1

        sub_list = [{'id': sub.id, 'status': sub.status,
            'date': sub.submit_time.astimezone(pytz.timezone('Asia/Shanghai'))
                .strftime("%Y-%m-%d %H:%M:%S")} for sub in current_subs]

        return render(request, 'submission/my_submission.html',
                      {'sub_list': sub_list, 'page': page, 'total_pages': total_pages})


class MySubmissionDetailView(View):
    def get(self, request, submission_id, problem_id=None):
        """
        查看具体提交
        :param request:
        :param submission_id:
        :param problem_id:
        :return:
        """
        try:
            submission = Submission.objects.get(id=submission_id)

        except Exception, e:
            return HttpResponseRedirect("/submissions")
        return render(request, 'submission/my_submission_detail.html')