#-*- coding:utf-8 -*-

from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Problem


class ProblemView(View):
    def get(self, request, *args, **kwargs):
        problem = Problem.objects.filter(contest_id=-1)

        problem_list = [{'id': p.id, 'title': p.title} for p in problem]

        return render_to_response('web_ide/problem_list.html',
                                  {'problem_list': problem_list}, RequestContext(request))


class ProblemSingleView(View):
    def get(self, request, problem_id, *args, **kwargs):
        problem = Problem.objects.get(id=problem_id)

        problem_info = {'title': problem.title, 'id': problem.id, 'descripion': problem.description,
                        'input_desc': problem.input_description, 'output_desc': problem.output_description,
                        'sample_input': problem.sample_input, 'sample_output': problem.sample_output}
        return render_to_response('web_ide/problem_single.html', {'problem': problem_info})

    def post(self, request):
        """
        提交题目接口
        :param request:
        :return:
        """
        pass
