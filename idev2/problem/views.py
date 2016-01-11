#-*- coding:utf-8 -*-

from django.views.generic import View
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from .models import Problem
from submission.models import Submission


class ProblemView(View):
    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:  {'problem_list': {'id': '', 'title': '', 'pass_ratio': '10%', 'submission': '1/10', 'date': ''}}
        """
        problem_set = Problem.objects.filter(contest_id=-1)

        problem_list = []
        for problem in problem_set:
            problem_info = {'id': problem.id,
                            'title': problem.title}
            all_subs = Submission.objects.filter(problem_id=problem.id)
            pass_subs = all_subs.filter(status='accepted')
            problem_info['pass_ratio'] = "%.2f"%(len(pass_subs) * 100.0 / len(all_subs)) if len(all_subs) > 0 else 0.0
            problem_info['submission'] = "/".join([str(len(pass_subs)), str(len(all_subs))])
            problem_info['date'] = problem.last_update.strftime("%Y-%m-%d")
            problem_list.append(problem_info)

        return render(request, 'web_ide/problem_list.html', {'problem_list': problem_list})


class ProblemSingleView(View):
    def get(self, request, problem_id, *args, **kwargs):
        problem = Problem.objects.get(id=problem_id)

        problem_info = {'title': problem.title, 'id': problem.id, 'description': problem.description,
                        'input_desc': problem.input_description, 'output_desc': problem.output_description,
                        'sample_input': problem.sample_input, 'sample_output': problem.sample_output}
        return render(request, 'web_ide/problem_single.html', {'problem': problem_info})

    def post(self, request):
        """
        提交题目接口
        :param request:
        :return:
        """
        pass
