from django.conf.urls import patterns, include, url
from django.contrib import admin

from problem.views import ProblemView, ProblemSingleView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'idev2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('web_ide.views',
    url(r'^$', 'index'),

    url(r'^code/submit/$', 'code_submit'),
)

urlpatterns += patterns('',
    url(r'^problems', ProblemView.as_view()),
    url(r'^problem/(?P<problem_id>\d+)', ProblemSingleView.as_view()),
)
