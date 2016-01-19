#-*- coding:utf-8 -*-

from datetime import datetime
import pytz
from hashlib import md5

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Problem
from submission.models import Submission
from contest.models import Contest

from global_util.util import date_to_string, get_total_page
from global_util.problem_util import problem_auth_check
from code_util.util import save_case_file

from idev2.settings import ITEMS_PER_PAGE, CASE_ROOT_PATH


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
            problem_info['date'] = date_to_string(problem.last_update)
            problem_list.append(problem_info)

        return render(request, 'web_ide/problem_list.html', {'problem_list': problem_list})


class ProblemSingleView(View):
    @problem_auth_check
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
        all_contest_list = Contest.objects.filter(end__gte=datetime.now(tz=pytz.timezone('Asia/Shanghai')))

        contest_list = [{'id': contest.id, 'name': contest.name} for contest in all_contest_list]
        contest_list.insert(0, {'id': -1, 'name': u'无'})

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
                                'memory_limit': problem.memory_limit, 'time_limit': problem.time_limit,
                                'contest_id': problem.contest_id}

                return render(request, 'admin/problem_edit.html',
                              {'problem': problem_info, 'contest_list': contest_list})
            except:
                return render(request, 'admin/problem_edit.html', {'contest_list': contest_list})
        return render(request, 'admin/problem_edit.html', {'contest_list': contest_list})

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
        problem_memory_limit = request.POST.get('memory_limit', '10000')
        problem_time_limit = request.POST.get('time_limit', '10000')
        problem_file = request.FILES.get('problem_case_file')

        problem_contest_id = int(request.POST.get('contest_id', '-1'))

        if problem_id:
            #更新习题信息
            try:
                problem = Problem.objects.get(id=problem_id)
            except:
                return HttpResponseRedirect('/admin/problem/home')
        else:
            #新建习题
            problem = Problem()
            problem.created_time = datetime.now(tz=pytz.timezone('Asia/Shanghai'))
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
        problem.contest_id = problem_contest_id

        #生成case_code
        #上传的文件存储到目录
        if problem_file and problem_file.size > 0:
            case_code = save_case_file(problem_file)
            problem.test_case_code = case_code

        #其他字段
        problem.tags = ""

        try:
            problem.save()
        except Exception, e:
            #create failed
            print e
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

    all_problem_objs = Problem.objects.all()

    total_pages = get_total_page(len(all_problem_objs))

    problem_objects = all_problem_objs.order_by('-last_update')\
        [(page-1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]

    problem_list = [{'id': problem.id, 'title': problem.title, 'contest_id': problem.contest_id,
                     'last_update': date_to_string(problem.last_update),
                     'create_time': date_to_string(problem.created_time)}
                    for problem in problem_objects]

    return render(request, 'admin/problem_home.html', {'problem_list': problem_list})