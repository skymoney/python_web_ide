#-*- coding:utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse, JsonResponse

from submission.models import Submission

from global_util.submission_util import submission_auth_check


class SubmissionQueryView(View):
    @submission_auth_check
    def post(self, request):
        """
        提供提交状态查询接口
        :param request: {'submission_id': ''}
        :return:
        """
        submission_id = request.POST.get('submission_id')

        try:
            submission = Submission.objects.get(id=submission_id)
            return JsonResponse({'status': 'ok', 'data': submission.status})
        except:
            return JsonResponse({'status': 'error', 'data': u'提交记录不存在'})