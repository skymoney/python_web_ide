#-*- coding:utf-8 -*-

from django.http import HttpResponseRedirect


def login_required(f):
    def wrapper(request, *args, **kwargs):
        if request.session.has_key('account'):
            return f(request, *args, **kwargs)
        return HttpResponseRedirect("/login?from=")
    return wrapper


def login_required_class(f):
    def wrapper(self, request, *args, **kwargs):
        if request.session.has_key('account'):
            return f(self, request, *args, **kwargs)
        return HttpResponseRedirect('/login?from=')
    return wrapper
