from django.conf.urls import patterns, include, url
from django.contrib import admin

from problem.views import ProblemView, ProblemSingleView
from submission.views import SubmissionQueryView
from docker_util.views import RuntimeMachineCheck
from account.views import AccountLoginView, AccountRegisterView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'idev2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('account.views',
    url(r'^logout/$', 'logout'),

    url(r'^account/active/$', 'active_account'),
    url(r'^login/$', AccountLoginView.as_view()),
    url(r'^register/$', AccountRegisterView.as_view()),
)

urlpatterns += patterns('web_ide.views',
    url(r'^$', 'index'),

    url(r'^code/submit/$', 'code_submit'),
)

urlpatterns += patterns('',
    url(r'^problems', ProblemView.as_view()),
    url(r'^problem/(?P<problem_id>\d+)', ProblemSingleView.as_view()),
)

urlpatterns += patterns('',
    url(r'^api/submission/query/$', SubmissionQueryView.as_view()),
    url(r'^api/runtime/check/$', RuntimeMachineCheck.as_view()),
)
