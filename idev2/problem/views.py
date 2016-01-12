#-*- coding:utf-8 -*-

from datetime import datetime
import pytz

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Problem
from submission.models import Submission

from idev2.settings import ITEMS_PER_PAGE


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
            problem_info['date'] = problem.last_update.astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d")
            problem_list.append(problem_info)

        return render(request, 'web_ide/problem_list.html', {'problem_list': problem_list})


class ProblemSingleView(View):
    def get(self, request, problem_id, *args, **kwargs):
        problem = Problem.objects.get(id=problem_id)

        problem_info = {'title': problem.title, 'id': problem.id, 'description': problem.description,
                        'input_desc': problem.input_description, 'output_desc': problem.output_description,
                        'hints': problem.hints,
                        'sample_input': problem.sample_input, 'sample_output': problem.sample_output}
        return render(request, 'web_ide/problem_single.html', {'problem': problem_info})

    def post(self, request):
        """
        提交题目接口
        :param request:
        :return:
        """
        pass


class ProblemAdminView(View):
    """
    管理员操作题目
    """
    def get(self, request, problem_id=None):
        if problem_id:
            #编辑题目信息
            try:
                problem = Problem.objects.get(id=problem_id)

                problem_info = {'id': problem.id, 'problem_title': problem.title,
                                'description': problem.description,
                                'input_description': problem.input_description,
                                'output_description': problem.output_description,
                                'sample_input': problem.sample_input, 'sample_output': problem.sample_output,
                                'hints': problem.hints,
                                'memory_limit': problem.memory_limit, 'time_limit': problem.time_limit}

                return render(request, 'admin/problem_edit.html', {'problem': problem_info})
            except:
                return render(request, 'admin/problem_edit.html')
        return render(request, 'admin/problem_edit.html')

    def post(self, request, problem_id=None):
        """
        更新/新建习题
        :param request:
        :return:
        """
        problem_id = request.POST.get('problem_id')
        problem_title = request.POST.get('problem_title')
        problem_description = request.POST.get('problem_description')
        problem_input = request.POST.get('input_description')
        problem_output = request.POST.get('output_description')
        problem_hints = request.POST.get('hints')
        problem_sample_input = request.POST.get('sample_input')
        problem_sample_output = request.POST.get('sample_output')
        problem_memory_limit = request.POST.get('memory_limit')
        problem_time_limit = request.POST.get('time_limit')

        problem_contest_id = request.POST.get('contest_Id') #TODO

        if problem_id:
            #更新习题信息
            try:
                problem = Problem.objects.get(id=problem_id)
                problem.title = problem_title
                problem.description = problem_description
                problem.input_description = problem_input
                problem.output_description = problem_output
                problem.hints = problem_hints
                problem.sample_input = problem_sample_input
                problem.sample_output = problem_sample_output
                problem.memory_limit = int(problem_memory_limit)
                problem.time_limit = int(problem_time_limit)

                problem.last_update = datetime.now(tz=pytz.timezone('Asia/Shanghai'))

                problem.save()

                return HttpResponseRedirect('/admin/problem/home')
            except:
                return HttpResponseRedirect('/admin/problem/home')

        #新建习题
        problem = Problem()
        problem.title = problem_title
        problem.description = problem_description
        problem.input_description = problem_input
        problem.output_description = problem_output
        problem.hints = problem_hints
        problem.sample_input = problem_sample_input
        problem.sample_output = problem_sample_output
        problem.memory_limit = int(problem_memory_limit)
        problem.time_limit = int(problem_time_limit)

        problem.created_time = datetime.now(tz=pytz.timezone('Asia/Shanghai'))
        problem.last_update = datetime.now(tz=pytz.timezone('Asia/Shanghai'))

        #生成case_code
        problem.test_case_code = '' #TODO

        #其他字段
        problem.tags = ""

        try:
            problem.save()
        except:
            #create failed
            pass
        return HttpResponseRedirect('/admin/problem/home')


def admin_problem_home(request):
    """
    显示所有习题，包括比赛下的
    :param request:
    :return:
    """
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    if page < 1:
        page = 1

    problem_objects = Problem.objects.all().order_by('-last_update')\
        [(page-1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]

    problem_list = [{'id': problem.id, 'title': problem.title, 'contest_id': problem.contest_id,
                     'last_update': problem.last_update.
                         astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S"),
                     'create_time': problem.created_time.
                         astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")}
                    for problem in problem_objects]

    return render(request, 'admin/problem_home.html', {'problem_list': problem_list})