#-*- coding:utf-8 -*-

from datetime import datetime
import pytz
import random
import math

from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

from .models import Contest, ContestJoin, ContestRandomProblems
from problem.models import Problem
from submission.models import Submission

from idev2.settings import ITEMS_PER_PAGE
from global_util.util import get_current_page, get_total_page, date_to_string
from global_util.auth_util import login_required_class


class ContestHomeView(View):
    def get(self, request):
        account = request.session.get('account')

        page = get_current_page(request.GET.get('page'))

        contest_all = Contest.objects.filter(end__gte=datetime.now(tz=pytz.timezone('Asia/Shanghai')))\
            .order_by('-end')

        current_contest_objects = contest_all[(page-1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE ]

        contest_list = []

        for contest in current_contest_objects:
            filtered_join = ContestJoin.objects.filter(contest_id=contest.id)
            joined_count = len(filtered_join)
            is_joined = 1 if account and len(filtered_join.filter(account_id=account['id'])) > 0 else 0

            contest_list.append({'id': contest.id, 'name': contest.name,
                                 'start': date_to_string(contest.start),
                                 'end': date_to_string(contest.end),
                                 'total_join': joined_count,
                                 'is_joined': is_joined})

        return render(request, 'contest/contest_home.html', {'contest_list': contest_list})


class ContestDetailView(View):
    @login_required_class
    def get(self, request, contest_id):
        account = request.session['account']
        try:
            contest = Contest.objects.get(id=contest_id)
            if len(ContestJoin.objects.filter(contest_id=contest.id, account_id=account['id'])) > 0:
                is_join = 1
            else:
                is_join = 0

            contest_info = {'id': contest.id, 'name': contest.name, 'description': contest.description,
                            'start': date_to_string(contest.start),
                            'end': date_to_string(contest.end),
                            'is_join': is_join}
            if contest.start > datetime.now(tz=pytz.timezone('Asia/Shanghai')):
                return render(request, 'contest/contest_detail.html', {'is_open': 0, 'contest': contest_info})

            if contest.random:
                #如果是随机比赛，从随机比赛表中读取
                all_crp = ContestRandomProblems.objects.filter(account_id=account['id'], contest_id=contest_id)
                problem_list = [crp.problem for crp in all_crp]
            else:
                problem_list = Problem.objects.filter(contest_id=contest.id)
            problem_info = []
            for problem in problem_list:
                all_subs = Submission.objects.filter(problem_id=problem.id)
                pass_subs = all_subs.filter(status='accepted')
                is_pass = 1 if len(pass_subs.filter(account_id=account['id'])) > 0 else 0
                problem_info.append({'id': problem.id, 'title': problem.title,
                                    'pass_ratio': '/'.join([str(len(pass_subs)), str(len(all_subs))]),
                                    'is_pass': is_pass})
            return render(request, 'contest/contest_detail.html',
                          {'contest': contest_info, 'problem_list': problem_info, 'is_open': 1})
        except Exception, e:
            print e
            return HttpResponseRedirect('/contest/home')

    @login_required_class
    def post(self, request):
        """
        参加比赛
        :param request: {'contest_id': ''}
        :return:
        """
        contest_id = request.POST.get('contest_id')
        account = request.session['account']

        if len(Contest.objects.filter(id=contest_id)) == 0:
            return JsonResponse({'status': 'error', 'data': u'比赛不存在'})

        if len(ContestJoin.objects.filter(contest_id=contest_id, account_id=account['id'])) > 0:
            return JsonResponse({'status': 'error', 'data': u'已经参加了该比赛'})
        contest = Contest.objects.get(id=contest_id)

        if contest.random:
            #随机比赛，需要分配题目
            all_problem_list = Problem.objects.filter(contest_id=contest.id)

            in_idx = []
            for i in xrange(contest.problem_nums):
                cur_idx = random.randint(0, len(all_problem_list)-1)
                while cur_idx in in_idx:
                    cur_idx = random.randint(0, len(all_problem_list)-1)
                in_idx.append(cur_idx)
                crp = ContestRandomProblems(contest_id=contest.id,
                        account_id=account['id'], problem=all_problem_list[cur_idx])

                try:
                    crp.save()
                except Exception, e:
                    #TODO 注意SQL事务
                    return JsonResponse({'status': 'error', 'data': u'出现错误，请稍后再试'})
        contest_join = ContestJoin(contest_id=contest_id, account_id=account['id'],
                                   join_time=datetime.now(tz=pytz.timezone('Asia/Shanghai')))

        try:
            contest_join.save()

            return JsonResponse({'status': 'ok', 'data': u'已经成功参加比赛'})
        except Exception, e:
            return JsonResponse({'status': 'error', 'data': u'出现错误，请稍后再试'})


class ContestAdminDetailView(View):
    def get(self, request, contest_id=None):
        if contest_id:
            try:
                contest = Contest.objects.get(id=contest_id)
                contest_info = {'id': contest.id, 'name': contest.name,
                                'description': contest.description,
                                'problem_nums': contest.problem_nums,
                                'start': date_to_string(contest.start),
                                'end': date_to_string(contest.end),
                                'create': date_to_string(contest.create_time),
                                'random': 1 if contest.random else 0}
                return render(request, 'admin/contest_edit.html', {'contest': contest_info})
            except Exception, e:
                return HttpResponseRedirect('/admin/contest/home')

        #新建比赛
        return render(request, 'admin/contest_edit.html')

    def post(self, request):
        #新建或者更新比赛POST
        contest_id = request.POST.get('contest_id')
        if contest_id:
            #更新比赛
            try:
                contest = Contest.objects.get(id=contest_id)
            except Exception, e:
                return HttpResponseRedirect('/admin/contest/home')
        else:
            contest = Contest()
        contest_name = request.POST.get('contest_name')
        contest_description = request.POST.get('contest_description')
        contest_problem_nums = request.POST.get('problem_nums')
        contest_random = True if int(request.POST.get('contest_random')) == 1 else False
        contest_start = datetime.strptime(request.POST.get('start'), '%Y-%m-%d %H:%M:%S')
        contest_end = datetime.strptime(request.POST.get('start'), '%Y-%m-%d %H:%M:%S')

        contest.name = contest_name
        contest.description = contest_description
        contest.problem_nums = contest_problem_nums
        contest.random = contest_random
        contest.start = contest_start
        contest.end = contest_end
        contest.create_time = datetime.now(tz=pytz.timezone('Asia/Shanghai'))

        try:
            contest.save()
            return HttpResponseRedirect('/admin/contest/home')
        except Exception, e:
            return HttpResponseRedirect('/admin/contest/home')



def admin_contest_home(request):
    """
    比赛管理界面
    :param request:
    :return:
    """
    page = get_current_page(request.GET.get('page'))

    all_contest_objs = Contest.objects.all().order_by('-start')

    total_pages = get_total_page(len(all_contest_objs))

    cur_contest_objs = all_contest_objs[(page - 1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]

    contest_info = [{'id': contest.id, 'name': contest.name,
                     'start': date_to_string(contest.start),
                     'end': date_to_string(contest.end),
                     'create': date_to_string(contest.create_time),
                     'random': 1 if contest.random else 0,
                     'problem_nums': contest.problem_nums}
                    for contest in cur_contest_objs]

    return render(request, 'admin/contest_home.html', {'contest_list': contest_info, 'page': page,
                                                       'total_pages': total_pages})