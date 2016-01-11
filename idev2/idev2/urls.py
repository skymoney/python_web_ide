from django.conf.urls import patterns, include, url
from django.contrib import admin

from problem import views as problem_view
from submission import views as submission_view
from docker_util import views as docker_view
from account import views as account_view
from web_ide import views as web_ide_view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/problem/$', problem_view.ProblemAdminView.as_view()),
    url(r'^logout/$', account_view.logout),

    url(r'^account/active/$', account_view.active_account),
    url(r'^login/$', account_view.AccountLoginView.as_view()),
    url(r'^register/$', account_view.AccountRegisterView.as_view()),
    url(r'^$', web_ide_view.index),

    url(r'^code/submit/$', web_ide_view.code_submit),
    url(r'^problems', problem_view.ProblemView.as_view()),
    url(r'^problem/(?P<problem_id>\d+)/$', problem_view.ProblemSingleView.as_view()),

    url(r'^api/submission/query/$', submission_view.SubmissionQueryView.as_view()),
    url(r'^api/runtime/check/$', docker_view.RuntimeMachineCheck.as_view()),

    url(r'^submissions/$', submission_view.MySubmissionView.as_view()),
    url(r'^submission/(?P<submission_id>\d+)/$', submission_view.MySubmissionDetailView.as_view()),
    url(r'^problem/(?P<problem_id>\d+)/submissions/$', submission_view.MySubmissionView.as_view()),
    url(r'^problem/(?P<problem_id>\d+)/submission/(?P<submission_id>\d+)/$',
        submission_view.MySubmissionDetailView.as_view()),

]
