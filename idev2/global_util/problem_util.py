#-*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from problem.models import Problem
from contest.models import Contest


def problem_auth_check(f):
    def wrapper(self, request, problem_id, *args, **kwargs):
        try:
            problem = Problem.objects.get(id=problem_id)

            if not problem.visiable:
                return HttpResponseRedirect('/problems')

            if problem.contest_id != -1:
                contest = Contest.objects.get(id=problem.contest_id)

                if not contest.is_publish:
                    return HttpResponseRedirect('/problems')

            return f(self, request, problem_id, *args, **kwargs)
        except Exception, e:
            return HttpResponseRedirect('/problems')

    return wrapper